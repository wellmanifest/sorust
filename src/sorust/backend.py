"""PEP 517 backend: explicit Cython modules plus one atomic Cargo library.

Setuptools' backend class is the only private upstream API used here; its
run_setup hook lets consumers configure everything in pyproject.toml.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sysconfig
import tempfile
import tomllib
from pathlib import Path


def configuration(root: Path) -> dict:
    document = tomllib.loads((root / "pyproject.toml").read_text())
    config = document["tool"]["sorust"]
    expected = {"python-modules", "rust-manifest", "rust-library", "artifact-package", "abi-version"}
    if set(config) != expected or config["abi-version"] != 1:
        raise ValueError("tool.sorust requires the v1 dual-artifact configuration")
    dotted = r"[a-zA-Z_]\w*(?:\.[a-zA-Z_]\w*)*"
    modules = config["python-modules"]
    if (not isinstance(modules, list) or not modules or len(set(modules)) != len(modules)
            or any(not isinstance(x, str) or not re.fullmatch(dotted, x) for x in modules)):
        raise ValueError("python-modules must contain unique dotted module names")
    package = config["artifact-package"]
    if not re.fullmatch(dotted, package) or any(not x.startswith(package + ".") for x in modules):
        raise ValueError("compiled modules must belong to artifact-package")
    if not re.fullmatch(r"[a-zA-Z_]\w*", config["rust-library"]):
        raise ValueError("invalid Rust library name")
    manifest = Path(config["rust-manifest"])
    if manifest.is_absolute() or ".." in manifest.parts:
        raise ValueError("Rust manifest must remain inside the project")
    lockfile = manifest.parent / "Cargo.lock"
    paths = [manifest, *(Path("src", *x.split(".")).with_suffix(".py") for x in modules), lockfile]
    for path in paths:
        full = root / path
        if path == lockfile and not full.is_file():
            raise ValueError("Rust component requires a committed Cargo.lock")
        if (not full.is_file() or any(p.is_symlink() for p in [full, *full.parents])
                or not full.resolve().is_relative_to(root.resolve())):
            raise ValueError(f"missing or unsafe source: {path}")
    return config


def _setup(wheel_staging: Path | None = None):
    from Cython.Build import cythonize
    from setuptools import Extension, setup
    from setuptools.command.build_ext import build_ext

    root = Path.cwd().resolve()
    config = configuration(root)
    package = config["artifact-package"]

    class DualBuild(build_ext):
        def run(self):
            if self.inplace:
                raise ValueError("Sorust uses installable wheels; in-place builds are unsupported")
            super().run()
            for name in config["python-modules"]:
                Path(self.build_lib).joinpath(*name.split(".")).with_suffix(".py").unlink(missing_ok=True)
            cargo_target = Path(self.build_temp).resolve() / "cargo"
            result = subprocess.run([
                "cargo", "build", "--release", "--locked", "--offline", "--lib",
                "--manifest-path", config["rust-manifest"],
                "--target-dir", str(cargo_target), "--message-format=json-render-diagnostics",
            ], check=True, capture_output=True, text=True)
            binaries = []
            for line in result.stdout.splitlines():
                message = json.loads(line)
                if (message.get("reason") == "compiler-artifact"
                        and message["target"]["name"] == config["rust-library"]):
                    binaries.extend(Path(x) for x in message["filenames"]
                                    if Path(x).suffix in {".so", ".dylib", ".dll"})
            if len(binaries) != 1:
                raise ValueError("Cargo must produce exactly one configured cdylib")
            package_root = Path(self.build_lib).joinpath(*package.split("."))
            destination = package_root / "_native" / binaries[0].name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(binaries[0], destination)
            headers = []
            for source in sorted((root / "include").glob("*.h")):
                header = destination.parent / source.name
                shutil.copyfile(source, header)
                headers.append(header)
            paths = [("python-extension", Path(self.get_ext_fullpath(x)))
                     for x in config["python-modules"]] + [("rust-cdylib", destination)]
            rustc = subprocess.check_output(["rustc", "-vV"], text=True)
            manifest = {
                "schema": "sorust.artifacts/v1", "abi_version": config["abi-version"],
                "package": package, "python_soabi": sysconfig.get_config_var("SOABI"),
                "platform": sysconfig.get_platform(), "rustc": rustc.strip(),
                "source_sha256": _source_digest(root, config),
                "headers": [{"path": path.relative_to(package_root).as_posix(),
                             "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for path in headers],
                "artifacts": [{"kind": kind, "path": path.relative_to(package_root).as_posix(),
                               "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                              for kind, path in paths],
            }
            manifest_path = package_root / "sorust-artifacts.json"
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
            self.extra_outputs = [str(destination), str(manifest_path), *map(str, headers)]

        def get_outputs(self):
            return super().get_outputs() + getattr(self, "extra_outputs", [])

    extensions = [Extension(name, [str(Path("src", *name.split(".")).with_suffix(".py"))])
                  for name in config["python-modules"]]
    commands = {"build_ext": DualBuild}
    if wheel_staging is not None:
        from setuptools.command.build import build
        from setuptools.command.bdist_wheel import bdist_wheel

        class WheelBuild(build):
            def finalize_options(self):
                super().finalize_options()
                self.build_lib = str(wheel_staging / "lib")

        class WheelDistribution(bdist_wheel):
            def finalize_options(self):
                super().finalize_options()
                self.bdist_dir = str(wheel_staging / "wheel")

            def run(self):
                if self.skip_build:
                    raise ValueError("Sorust wheel builds require a fresh build; --skip-build is unsupported")
                super().run()

        commands["build"] = WheelBuild
        commands["bdist_wheel"] = WheelDistribution
    setup(ext_modules=cythonize(extensions, build_dir="build/cython", language_level=3),
          cmdclass=commands)


def _source_digest(root: Path, config: dict) -> str:
    files = [root / "pyproject.toml", *sorted((root / "src").rglob("*.py"))]
    crate = root / Path(config["rust-manifest"]).parent
    files += [crate / "Cargo.toml", crate / "Cargo.lock", *sorted((crate / "src").rglob("*.rs"))]
    files += sorted((root / "include").glob("*.h"))
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.relative_to(root).as_posix().encode() + b"\0")
        digest.update(path.read_bytes() + b"\0")
    return digest.hexdigest()


def _backend(wheel_staging: Path | None = None):
    from setuptools.build_meta import _BuildMetaBackend

    class Backend(_BuildMetaBackend):
        def run_setup(self, setup_script="setup.py"):
            if Path(setup_script).exists():
                raise ValueError("Sorust consumers use pyproject.toml without setup.py")
            _setup(wheel_staging)

    return Backend()


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    # Reuse compiler caches, but never package payload from a previous build.
    build_root = Path.cwd().resolve() / "build"
    build_root.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="sorust-wheel-", dir=build_root) as staging:
        return _backend(Path(staging)).build_wheel(wheel_directory, config_settings, metadata_directory)


def build_sdist(sdist_directory, config_settings=None):
    return _backend().build_sdist(sdist_directory, config_settings)


def get_requires_for_build_wheel(config_settings=None):
    return ["setuptools>=77", "wheel>=0.45", "Cython>=3,<4"]


get_requires_for_build_sdist = get_requires_for_build_wheel


def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
    return _backend().prepare_metadata_for_build_wheel(metadata_directory, config_settings)
