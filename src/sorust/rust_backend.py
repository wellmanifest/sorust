"""PEP 517 producer for Rust-only components; no Cython or Python payload."""
from __future__ import annotations

import hashlib
import json
import sysconfig
from pathlib import Path

from . import verify_artifacts
from . import backend as shared


def configuration(root: Path) -> dict:
    return shared.configuration(root, native_only=True)


def _setup(wheel_staging: Path | None = None):
    from setuptools import Distribution, setup
    from setuptools.command.build_ext import build_ext

    root = Path.cwd().resolve()
    config = configuration(root)

    class RustDistribution(Distribution):
        def has_ext_modules(self):
            return True

        def has_pure_modules(self):
            return False

    class RustBuild(build_ext):
        def run(self):
            if self.inplace:
                raise ValueError("Sorust uses installable wheels; in-place builds are unsupported")
            package_root = Path(self.build_lib).joinpath(*config["artifact-package"].split("."))
            library, headers, rustc = shared._build_rust(root, config, self.build_temp, package_root)
            entry = lambda path: {"path": path.relative_to(package_root).as_posix(),
                                  "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            manifest = {"schema": "sorust.rust-component/v1", "abi_version": config["abi-version"],
                        "package": config["artifact-package"], "platform": sysconfig.get_platform(),
                        "rustc": rustc, "source_sha256": shared._source_digest(root, config),
                        "headers": [entry(path) for path in headers],
                        "artifacts": [dict(kind="rust-cdylib", **entry(library))]}
            path = package_root / "sorust-artifacts.json"
            path.write_text(json.dumps(manifest, indent=2) + "\n")
            verify_artifacts(package_root)
            self.extra_outputs = [str(library), str(path), *map(str, headers)]

        def get_source_files(self):
            return [path.relative_to(root).as_posix() for path in shared._source_files(root, config)]

        def get_outputs(self):
            return getattr(self, "extra_outputs", [])

    commands = shared._wheel_commands({"build_ext": RustBuild}, wheel_staging, native_only=True)
    setup(packages=[], py_modules=[], ext_modules=[], distclass=RustDistribution, cmdclass=commands)


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    return shared._build_wheel(wheel_directory, config_settings, metadata_directory, _setup)


def build_sdist(sdist_directory, config_settings=None):
    return shared._backend(setup_function=_setup).build_sdist(sdist_directory, config_settings)


def get_requires_for_build_wheel(config_settings=None):
    return ["setuptools>=77", "wheel>=0.45"]


get_requires_for_build_sdist = get_requires_for_build_wheel


def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
    return shared._backend(setup_function=_setup).prepare_metadata_for_build_wheel(metadata_directory, config_settings)
