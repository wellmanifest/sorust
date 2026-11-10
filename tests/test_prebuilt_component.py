"""Installed Rust dependencies are pinned, snapshotted and reused, never built."""
import copy
import hashlib
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import sysconfig
import tarfile
from types import SimpleNamespace
import venv
import zipfile

import pytest
import sorust.backend as backend
from test_build import ROOT, built, external_project, run


def component_project(project, spec):
    path = project / "pyproject.toml"
    text = path.read_text().replace('rust-manifest = "crates/sorust-kernel/Cargo.toml"\n', '', 1)
    text += '\n[tool.sorust.rust-component]\n' + ''.join(f'{key} = {json.dumps(value)}\n' for key, value in spec.items())
    path.write_text(text)


@pytest.fixture
def donor(tmp_path, monkeypatch):
    site = tmp_path / "installed"
    package = site / "kernel_pkg"
    files = {"__init__.py": b'raise AssertionError("donor package imported")\n',
             "module.so": b"unused Python extension", "_native/libsorust_kernel.so": b"Rust bytes",
             "_native/sorust.h": b"header bytes"}
    for name, data in files.items():
        path = package / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    entry = lambda name: {"path": name, "sha256": hashlib.sha256(files[name]).hexdigest()}
    manifest = {"schema": "sorust.artifacts/v1", "abi_version": 1, "package": "kernel_pkg",
                "platform": sysconfig.get_platform(), "rustc": "rustc fixture", "source_sha256": "a" * 64,
                "artifacts": [dict(kind="python-extension", **entry("module.so")),
                              dict(kind="rust-cdylib", **entry("_native/libsorust_kernel.so"))],
                "headers": [entry("_native/sorust.h")]}
    installed = SimpleNamespace(version="1.2.3", metadata={"Name": "fixture-kernel"},
                                files=[Path("kernel_pkg") / name for name in [*files, "sorust-artifacts.json"]])
    installed.site = site
    installed.locate_file = lambda relative: installed.site / relative
    spec = {"distribution": "fixture-kernel", "version": "1.2.3", "package": "kernel_pkg", "manifest-sha256": ""}

    def pin():
        raw = (json.dumps(manifest, indent=2) + "\n").encode()
        (package / "sorust-artifacts.json").write_bytes(raw)
        spec["manifest-sha256"] = hashlib.sha256(raw).hexdigest()

    pin()
    monkeypatch.setattr(backend.metadata, "distribution", lambda name: installed)
    monkeypatch.syspath_prepend(str(site))
    config = {"rust-component": spec, "abi-version": 1, "rust-library": "sorust_kernel"}
    return SimpleNamespace(site=site, package=package, installed=installed, manifest=manifest,
                           spec=spec, config=config, pin=pin)


def test_component_does_not_import_donor_and_snapshots_owned_files(donor):
    assert "kernel_pkg" not in sys.modules
    snapshot = backend._rust_component(donor.config)
    assert "kernel_pkg" not in sys.modules
    assert snapshot["payload"] == {Path("_native/libsorust_kernel.so"): b"Rust bytes",
                                   Path("_native/sorust.h"): b"header bytes"}
    assert snapshot["provenance"]["distribution"] == "fixture-kernel"
    assert snapshot["provenance"]["manifest_sha256"] == donor.spec["manifest-sha256"]


@pytest.mark.parametrize("invalid", [None, {}, "package", {"distribution": "bad/name"},
    {"manifest-sha256": "a" * 63}, {"manifest-sha256": "A" * 64}, {"package": "../kernel"}])
def test_component_rejects_malformed_descriptor(donor, invalid):
    config = copy.deepcopy(donor.config)
    if isinstance(invalid, dict) and invalid:
        config["rust-component"].update(invalid)
    else:
        config["rust-component"] = invalid
    with pytest.raises(ValueError, match="rust-component"):
        backend._rust_component(config)


@pytest.mark.parametrize("case", ["version", "distribution", "pin", "package", "platform", "library",
                                  "compiler", "source", "resources", "manifest-ownership", "payload-ownership",
                                  "manifest-link", "parent-link", "payload-drift", "header-layout", "duplicate-header"])
def test_component_rejects_wrong_or_unsafe_dependency(donor, case):
    if case == "version":
        donor.spec["version"] = "9.0"
    elif case == "distribution":
        donor.installed.metadata["Name"] = "other-distribution"
    elif case == "pin":
        donor.spec["manifest-sha256"] = "0" * 64
    elif case in {"package", "platform", "compiler", "source"}:
        key, value = {"package": ("package", "other"), "platform": ("platform", "other-platform"),
                      "compiler": ("rustc", ""), "source": ("source_sha256", "not-a-pin")}[case]
        donor.manifest[key] = value
        donor.pin()
    elif case == "library":
        donor.config["rust-library"] = "other_kernel"
    elif case == "resources":
        path = donor.package / "data.json"
        path.write_bytes(b'{}')
        donor.manifest.update(schema="sorust.artifacts/v2",
                              resources=[{"path": "data.json", "sha256": hashlib.sha256(b'{}').hexdigest()}])
        donor.pin()
    elif case.endswith("ownership"):
        relative = "sorust-artifacts.json" if case == "manifest-ownership" else "_native/libsorust_kernel.so"
        donor.installed.files.remove(Path("kernel_pkg") / relative)
    elif case == "manifest-link":
        path = donor.package / "sorust-artifacts.json"
        saved = donor.package / "saved.json"
        path.rename(saved)
        path.symlink_to(saved)
    elif case == "parent-link":
        (donor.package / "_native").rename(donor.package / "actual")
        (donor.package / "_native").symlink_to(donor.package / "actual", target_is_directory=True)
    elif case == "payload-drift":
        (donor.package / "_native/libsorust_kernel.so").write_bytes(b"changed")
    elif case == "header-layout":
        path = donor.package / "_native/nested/sorust.h"
        path.parent.mkdir()
        path.write_bytes(b"header bytes")
        donor.manifest["headers"][0]["path"] = "_native/nested/sorust.h"
        donor.pin()
    else:
        donor.manifest["headers"] *= 2
        donor.pin()
    with pytest.raises(ValueError, match="component"):
        backend._rust_component(donor.config)


def test_component_missing_distribution_is_configuration_error(donor, monkeypatch):
    def absent(name):
        raise backend.metadata.PackageNotFoundError(name)
    monkeypatch.setattr(backend.metadata, "distribution", absent)
    with pytest.raises(ValueError, match="component"):
        backend._rust_component(donor.config)


@pytest.mark.parametrize("change", ["manifest", "payload"])
def test_component_rechecks_pinned_manifest_and_payload_snapshot(donor, monkeypatch, change):
    original = backend.verify_artifacts

    def race(root):
        if change == "manifest":
            donor.manifest["source_sha256"] = "b" * 64
            (root / "sorust-artifacts.json").write_text(json.dumps(donor.manifest))
            return original(root)
        manifest = original(root)
        (root / "_native/libsorust_kernel.so").write_bytes(b"changed after verification")
        return manifest

    monkeypatch.setattr(backend, "verify_artifacts", race)
    with pytest.raises(ValueError, match="changed"):
        backend._rust_component(donor.config)


def test_component_fingerprint_uses_snapshot_and_excludes_install_location(donor, tmp_path):
    project, _, _ = external_project(tmp_path)
    shutil.rmtree(project / "crates")
    shutil.rmtree(project / "include")
    component_project(project, donor.spec)
    config = backend.configuration(project)
    snapshot = backend._rust_component(config)
    expected = backend._source_digest(project, config, snapshot)
    relocated = tmp_path / "other-install"
    shutil.copytree(donor.site, relocated)
    donor.installed.site = relocated
    assert backend._source_digest(project, config) == expected
    (relocated / "kernel_pkg/_native/libsorust_kernel.so").write_bytes(b"changed")
    assert backend._source_digest(project, config, snapshot) == expected
    with pytest.raises(ValueError, match="component"):
        backend._source_digest(project, config)


@pytest.mark.parametrize("case", ["both", "neither", "local-headers"])
def test_component_configuration_requires_one_mode_and_canonical_headers(donor, tmp_path, case):
    project, _, _ = external_project(tmp_path)
    if case != "local-headers":
        shutil.rmtree(project / "include")
    if case == "neither":
        path = project / "pyproject.toml"
        path.write_text(path.read_text().replace('rust-manifest = "crates/sorust-kernel/Cargo.toml"\n', ''))
    else:
        component_project(project, donor.spec)
        if case == "both":
            path = project / "pyproject.toml"
            path.write_text(path.read_text().replace('rust-library = "sorust_kernel"',
                'rust-library = "sorust_kernel"\nrust-manifest = "crates/sorust-kernel/Cargo.toml"'))
    with pytest.raises(ValueError, match="component"):
        backend.configuration(project)


@pytest.mark.parametrize("resources", [False, True])
def test_component_source_sdist_and_wheel_without_rust_tools(built, tmp_path, resources):
    _, wheel, python, installed_package = built
    run([sys.executable, "-I", "-m", "pip", "install", "--no-deps", "--force-reinstall", wheel])
    with zipfile.ZipFile(wheel) as archive:
        raw = archive.read("sorust/sorust-artifacts.json")
    donor_manifest = json.loads(raw)
    spec = {"distribution": "sorust", "version": "0.1.0", "package": "sorust",
            "manifest-sha256": hashlib.sha256(raw).hexdigest()}
    project, package, _ = external_project(tmp_path)
    shutil.rmtree(project / "crates")
    shutil.rmtree(project / "include")
    if resources:
        (package / "settings.json").write_text('{"factor":7}')
        (package / "_compat.py").write_text('from pathlib import Path\nimport json\n'
            'def double(value):\n    return value * json.loads(Path(__file__).with_name("settings.json").read_bytes())["factor"]\n')
        path = project / "pyproject.toml"
        path.write_text(path.read_text().replace('abi-version = 1', 'abi-version = 1\nresources = ["settings.json"]'))
    component_project(project, spec)
    tools = tmp_path / "no-rust"
    tools.mkdir()
    marker = tmp_path / "rust-called"
    for name in ["cargo", "rustc"]:
        path = tools / name
        path.write_text(f"#!/bin/sh\nprintf '%s\\n' {name} >> {shlex.quote(str(marker))}\nexit 97\n")
        path.chmod(0o755)
    import os
    env = dict(os.environ, PATH=str(tools) + os.pathsep + os.environ.get("PATH", ""))
    env.pop("PYTHONPATH", None)
    output = tmp_path / "dist"
    result = subprocess.run([sys.executable, "-I", "-m", "build", "--no-isolation", "--outdir", str(output), str(project)],
                            cwd=ROOT, env=env, text=True, capture_output=True, timeout=180)
    assert result.returncode == 0, result.stdout + result.stderr
    assert not marker.exists(), "consumer build invoked a Rust tool"
    with tarfile.open(next(output.glob("*.tar.gz"))) as archive:
        assert not any(x.endswith((".so", ".dll", ".dylib")) or "/crates/" in x or "/include/" in x
                       for x in archive.getnames())
    consumer_wheel = next(output.glob("*.whl"))
    with zipfile.ZipFile(consumer_wheel) as archive:
        manifest = json.loads(archive.read("nl_atomic_example/sorust-artifacts.json"))
        assert manifest["schema"] == ("sorust.artifacts/v2" if resources else "sorust.artifacts/v1")
        assert manifest["rust_component"]["manifest_sha256"] == spec["manifest-sha256"]
        assert manifest["rust_component"]["source_sha256"] == donor_manifest["source_sha256"]
        assert manifest["rustc"] == donor_manifest["rustc"] and manifest["headers"] == donor_manifest["headers"]
        native = next(x for x in manifest["artifacts"] if x["kind"] == "rust-cdylib")
        assert native == next(x for x in donor_manifest["artifacts"] if x["kind"] == "rust-cdylib")
        for item in manifest["artifacts"] + manifest["headers"] + manifest.get("resources", []):
            assert hashlib.sha256(archive.read("nl_atomic_example/" + item["path"])).hexdigest() == item["sha256"]
    run([python, "-I", "-m", "pip", "install", "--no-deps", "--force-reinstall", consumer_wheel])
    exported = tmp_path / "standalone/nl_atomic_example"
    exported.parent.mkdir()
    run([python, "-I", "-c", '''
import ctypes, pathlib, sys, sorust
from nl_atomic_example import _compat
assert _compat.double(3) == int(sys.argv[2])
root = pathlib.Path(_compat.__file__).parent
manifest = sorust.verify_artifacts(root)
library = ctypes.CDLL(str(root / next(x["path"] for x in manifest["artifacts"] if x["kind"] == "rust-cdylib")))
library.sorust_abi_version.argtypes = []
library.sorust_abi_version.restype = ctypes.c_uint32
assert library.sorust_abi_version() == 1
destination = sorust.export_artifacts(sys.argv[1], package_dir=root)
assert sorust.verify_artifacts(destination) == manifest
''', exported, 21 if resources else 6])
    minimal = tmp_path / "runtime"
    venv.EnvBuilder(with_pip=False, symlinks=False).create(minimal)
    run([minimal / "bin/python", "-I", "-c", '''
import importlib.util, sys
sys.path.insert(0, sys.argv[1])
assert importlib.util.find_spec("sorust") is None
from nl_atomic_example import _compat
assert _compat.double(3) == int(sys.argv[2])
''', exported.parent, 21 if resources else 6])
