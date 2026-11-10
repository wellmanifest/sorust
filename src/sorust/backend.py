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
import sys
import sysconfig
import tempfile
import tomllib
from importlib import metadata
from pathlib import Path

from . import NativeArtifactError, _resource_path, verify_artifacts


def configuration(root: Path) -> dict:
    document = tomllib.loads((root / "pyproject.toml").read_text())
    config = document["tool"]["sorust"]
    if ("rust-manifest" in config) == ("rust-component" in config):
        raise ValueError("choose exactly one rust-manifest or rust-component")
    expected = {"python-modules", "rust-library", "artifact-package", "abi-version"}
    expected.add("rust-component" if "rust-component" in config else "rust-manifest")
    if (not expected.issubset(config) or set(config) - expected - {"resources"}
            or config["abi-version"] != 1):
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
    paths = [Path("src", *x.split(".")).with_suffix(".py") for x in modules]
    lockfile = None
    if "rust-manifest" in config:
        manifest = Path(config["rust-manifest"])
        if manifest.is_absolute() or ".." in manifest.parts:
            raise ValueError("Rust manifest must remain inside the project")
        lockfile = manifest.parent / "Cargo.lock"
        paths = [manifest, *paths, lockfile]
    for path in paths:
        full = root / path
        if path == lockfile and not full.is_file():
            raise ValueError("Rust component requires a committed Cargo.lock")
        if (not full.is_file() or any(p.is_symlink() for p in [full, *full.parents])
                or not full.resolve().is_relative_to(root.resolve())):
            raise ValueError(f"missing or unsafe source: {path}")
    if "rust-manifest" in config:
        _build_script(root, config)
    else:
        if list((root / "include").glob("*.h")):
            raise ValueError("prebuilt Rust component supplies its own headers; remove local include headers")
        _rust_component(config)
    _resource_files(root, config)
    return config


def _rust_component(config: dict) -> dict:
    """Snapshot a pinned installed component without importing its package."""
    spec = config["rust-component"]
    fields = {"distribution", "version", "package", "manifest-sha256"}
    if (not isinstance(spec, dict) or set(spec) != fields
            or not all(isinstance(spec.get(key), str) and spec[key] for key in fields)
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", spec["distribution"])
            or not re.fullmatch(r"[a-zA-Z_]\w*(?:\.[a-zA-Z_]\w*)*", spec["package"])
            or not re.fullmatch(r"[0-9a-f]{64}", spec["manifest-sha256"])):
        raise ValueError("rust-component requires distribution, exact version, package and manifest-sha256")
    canonical = lambda value: re.sub(r"[-_.]+", "-", value).lower()
    try:
        installed = metadata.distribution(spec["distribution"])
        if (installed.version != spec["version"]
                or canonical(installed.metadata["Name"]) != canonical(spec["distribution"])):
            raise ValueError("component distribution identity/version mismatch")
        owned = {str(path).replace("\\", "/") for path in installed.files or []}
        relative_package = Path(*spec["package"].split("."))
        manifest_relative = relative_package / "sorust-artifacts.json"
        if manifest_relative.as_posix() not in owned:
            raise ValueError("component manifest is not owned by the distribution")
        root = Path(installed.locate_file(relative_package))
        manifest_path = root / "sorust-artifacts.json"
        if any(path.is_symlink() for path in [manifest_path, *manifest_path.parents]):
            raise ValueError("component manifest path contains a symlink")
        raw = manifest_path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != spec["manifest-sha256"]:
            raise ValueError("component manifest pin mismatch")
        manifest = verify_artifacts(root)
        if manifest != json.loads(raw):
            raise ValueError("component manifest changed during verification")
        if (manifest["package"] != spec["package"] or manifest["abi_version"] != config["abi-version"]
                or manifest["platform"] != sysconfig.get_platform()):
            raise ValueError("component package, ABI or platform mismatch")
        if manifest.get("resources"):
            raise ValueError("prebuilt Rust component must be resource-free")
        if (not isinstance(manifest.get("rustc"), str) or not manifest["rustc"].strip()
                or not isinstance(manifest.get("source_sha256"), str)
                or not re.fullmatch(r"[0-9a-f]{64}", manifest["source_sha256"])):
            raise ValueError("component compiler/source provenance is missing")
        library = next(item for item in manifest["artifacts"] if item["kind"] == "rust-cdylib")
        suffix = ".dll" if sys.platform == "win32" else ".dylib" if sys.platform == "darwin" else ".so"
        prefix = "" if suffix == ".dll" else "lib"
        if library["path"] != f'_native/{prefix}{config["rust-library"]}{suffix}':
            raise ValueError("component Rust library identity mismatch")
        headers = manifest.get("headers", [])
        if any(Path(item["path"]).parent != Path("_native") or Path(item["path"]).suffix != ".h"
               for item in headers):
            raise ValueError("component headers must be direct _native/*.h files")
        payload = {}
        for item in [library, *headers]:
            relative = Path(item["path"])
            path = root / relative
            if ((relative_package / relative).as_posix() not in owned or relative in payload
                    or any(p.is_symlink() for p in [path, *path.parents])):
                raise ValueError("component payload is unowned, duplicated or linked")
            data = path.read_bytes()
            if hashlib.sha256(data).hexdigest() != item["sha256"]:
                raise ValueError("component payload changed before snapshot")
            payload[relative] = data
        provenance = {"distribution": canonical(spec["distribution"]), "version": installed.version,
                      "package": spec["package"], "manifest_sha256": spec["manifest-sha256"],
                      "source_sha256": manifest["source_sha256"]}
        return {"manifest": manifest, "manifest_bytes": raw, "payload": payload,
                "library": Path(library["path"]), "headers": [Path(x["path"]) for x in headers],
                "provenance": provenance}
    except (metadata.PackageNotFoundError, OSError, ValueError, KeyError, TypeError, NativeArtifactError) as error:
        raise ValueError(f"Invalid installed Rust component: {error}") from error


def _resource_files(root: Path, config: dict) -> list[Path]:
    resources = config.get("resources", [])
    if not isinstance(resources, list):
        raise ValueError("resources must be a list of unique package-relative paths")
    paths = [_resource_path(value) for value in resources]
    if len(set(paths)) != len(paths):
        raise ValueError("resources must contain unique paths")
    package_root = root.joinpath("src", *config["artifact-package"].split("."))
    files = []
    for relative in sorted(paths):
        full = package_root / relative
        if (not full.is_file() or any(p.is_symlink() for p in [full, *full.parents])
                or not full.resolve().is_relative_to(package_root.resolve())):
            raise ValueError(f"missing or unsafe resource: {relative}")
        files.append(full)
    return files


def _build_script(root: Path, config: dict) -> Path | None:
    crate = root / Path(config["rust-manifest"]).parent
    package = tomllib.loads((crate / "Cargo.toml").read_text()).get("package", {})
    if not isinstance(package, dict):
        raise ValueError("Cargo package must be a table")
    selected = package.get("build", True)
    if selected is False:
        return None
    if selected is True:
        path = crate / "build.rs"
        if "build" not in package and not path.exists() and not path.is_symlink():
            return None
    elif isinstance(selected, str) and selected and not Path(selected).is_absolute():
        path = crate / selected
    else:
        raise ValueError("Cargo build script must be a relative path or boolean")
    if (not path.is_file() or any(p.is_symlink() for p in [path, *path.parents])
            or not path.resolve().is_relative_to(root.resolve())):
        raise ValueError("missing or unsafe Cargo build script")
    return path.resolve()


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
            component = _rust_component(config) if "rust-component" in config else None
            super().run()
            for name in config["python-modules"]:
                Path(self.build_lib).joinpath(*name.split(".")).with_suffix(".py").unlink(missing_ok=True)
            package_root = Path(self.build_lib).joinpath(*package.split("."))
            if component is not None:
                for relative, data in component["payload"].items():
                    target = package_root / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(data)
                destination = package_root / component["library"]
                headers = [package_root / path for path in component["headers"]]
                rustc = component["manifest"]["rustc"]
            else:
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
                destination = package_root / "_native" / binaries[0].name
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(binaries[0], destination)
                headers = []
                for source in sorted((root / "include").glob("*.h")):
                    header = destination.parent / source.name
                    shutil.copyfile(source, header)
                    headers.append(header)
                rustc = subprocess.check_output(["rustc", "-vV"], text=True).strip()
            paths = [("python-extension", Path(self.get_ext_fullpath(x)))
                     for x in config["python-modules"]] + [("rust-cdylib", destination)]
            resources = []
            source_package = root.joinpath("src", *package.split("."))
            for source in _resource_files(root, config):
                target = package_root / source.relative_to(source_package)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
                resources.append(target)
            manifest = {
                "schema": "sorust.artifacts/v2" if resources else "sorust.artifacts/v1",
                "abi_version": config["abi-version"],
                "package": package, "python_soabi": sysconfig.get_config_var("SOABI"),
                "platform": sysconfig.get_platform(), "rustc": rustc.strip(),
                "source_sha256": _source_digest(root, config, component),
                "headers": [{"path": path.relative_to(package_root).as_posix(),
                             "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for path in headers],
                "artifacts": [{"kind": kind, "path": path.relative_to(package_root).as_posix(),
                               "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                              for kind, path in paths],
            }
            if component is not None:
                manifest["rust_component"] = component["provenance"]
            if resources:
                manifest["resources"] = [{"path": path.relative_to(package_root).as_posix(),
                                          "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                                         for path in resources]
            manifest_path = package_root / "sorust-artifacts.json"
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
            self.extra_outputs = [str(destination), str(manifest_path), *map(str, headers + resources)]

        def get_source_files(self):
            return super().get_source_files() + [str(path.relative_to(root))
                                               for path in _resource_files(root, config)]

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


def _source_digest(root: Path, config: dict, component: dict | None = None) -> str:
    files = [root / "pyproject.toml", *sorted((root / "src").rglob("*.py"))]
    if "rust-manifest" in config:
        crate = root / Path(config["rust-manifest"]).parent
        files += [crate / "Cargo.toml", crate / "Cargo.lock", *sorted((crate / "src").rglob("*.rs"))]
        files += sorted((root / "include").glob("*.h"))
        script = _build_script(root, config)
        if script is not None and script not in files:
            files.append(script)
    files += [path for path in _resource_files(root, config) if path not in files]
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.relative_to(root).as_posix().encode() + b"\0")
        digest.update(path.read_bytes() + b"\0")
    if "rust-component" in config:
        component = component if component is not None else _rust_component(config)
        spec = component["provenance"]
        prefix = f'rust-component/{spec["distribution"]}/{spec["version"]}/{spec["package"]}/'
        inputs = [("sorust-artifacts.json", component["manifest_bytes"]),
                  *((path.as_posix(), data) for path, data in component["payload"].items())]
        for name, data in inputs:
            digest.update((prefix + name).encode() + b"\0" + data + b"\0")
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
