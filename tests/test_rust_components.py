"""Rust-only manifests, real data-only wheels and legacy-reader boundaries."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import zipfile

import pytest
import sorust
from sorust import backend
from test_build import ROOT, built, run
from test_prebuilt_component import donor
from test_nl_dsl_pilot import pilot


@pytest.fixture
def native(donor):
    donor.manifest["schema"] = "sorust.rust-component/v1"
    donor.manifest["artifacts"] = [x for x in donor.manifest["artifacts"] if x["kind"] == "rust-cdylib"]
    for name in ["__init__.py", "module.so"]:
        (donor.package / name).unlink()
        donor.installed.files.remove(Path("kernel_pkg") / name)
    donor.pin()
    return donor


def test_native_manifest_verifies_exports_and_resolves_without_python(native, tmp_path):
    assert sorust.verify_artifacts(native.package) == native.manifest
    snapshot = backend._rust_component(native.config)
    assert "kernel_pkg" not in sys.modules
    assert set(snapshot["payload"]) == {Path("_native/libsorust_kernel.so"), Path("_native/sorust.h")}
    target = sorust.export_artifacts(tmp_path / "export", package_dir=native.package)
    assert sorust.verify_artifacts(target) == native.manifest
    assert {p.relative_to(target).as_posix() for p in target.rglob("*") if p.is_file()} == {
        "_native/libsorust_kernel.so", "_native/sorust.h", "sorust-artifacts.json"}


@pytest.mark.parametrize("case", ["python-artifact", "empty", "two-libraries", "resources", "soabi",
    "missing-source", "source", "package", "platform", "compiler", "headers", "abi-bool",
    "hash", "alias", "escape", "absolute", "backslash", "nested", "library-suffix", "header-suffix",
    "duplicate-header", "extra-entry-field", "metadata-link", "root-link", "parent-link", "payload-link", "drift", "missing"])
def test_native_manifest_rejects_ambiguous_or_unsafe_payload(native, tmp_path, case):
    m = native.manifest
    if case == "python-artifact":
        m["artifacts"].append(dict(kind="python-extension", path="module.so", sha256="a" * 64))
    elif case == "empty":
        m["artifacts"] = []
    elif case == "two-libraries":
        m["artifacts"] *= 2
    elif case in {"resources", "soabi"}:
        m["resources" if case == "resources" else "python_soabi"] = [] if case == "resources" else "cpython-313"
    elif case == "missing-source":
        del m["source_sha256"]
    elif case in {"source", "package", "platform", "compiler", "headers", "abi-bool"}:
        key, value = {"source": ("source_sha256", "A" * 64), "package": ("package", "../bad"),
                      "platform": ("platform", ""), "compiler": ("rustc", ""),
                      "headers": ("headers", {}), "abi-bool": ("abi_version", True)}[case]
        m[key] = value
    elif case == "hash":
        m["artifacts"][0]["sha256"] = "A" * 64
    elif case in {"alias", "escape", "absolute", "backslash", "nested", "library-suffix"}:
        m["artifacts"][0]["path"] = {"alias": "_native//libsorust_kernel.so", "escape": "../outside.so",
            "absolute": "/tmp/outside.so", "backslash": "_native\\libsorust_kernel.so",
            "nested": "_native/other/libsorust_kernel.so", "library-suffix": "_native/library.py"}[case]
    elif case == "header-suffix":
        m["headers"][0]["path"] = "_native/header.py"
    elif case == "duplicate-header":
        m["headers"] *= 2
    elif case == "extra-entry-field":
        m["artifacts"][0]["unverified"] = "other.so"
    native.pin()
    if case == "metadata-link":
        path = native.package / "sorust-artifacts.json"
        path.rename(native.package / "saved.json")
        path.symlink_to(native.package / "saved.json")
    elif case == "root-link":
        actual = native.package.with_name("actual-root")
        native.package.rename(actual)
        native.package.symlink_to(actual, target_is_directory=True)
    elif case == "parent-link":
        (native.package / "_native").rename(native.package / "actual")
        (native.package / "_native").symlink_to(native.package / "actual", target_is_directory=True)
    elif case == "payload-link":
        path = native.package / "_native/libsorust_kernel.so"
        path.rename(path.with_name("saved.so"))
        path.symlink_to(path.with_name("saved.so"))
    elif case == "drift":
        (native.package / "_native/libsorust_kernel.so").write_bytes(b"drift")
    elif case == "missing":
        (native.package / "_native/libsorust_kernel.so").unlink()
    target = tmp_path / "rejected"
    with pytest.raises(sorust.NativeArtifactError):
        sorust.verify_artifacts(native.package)
    with pytest.raises(sorust.NativeArtifactError):
        sorust.export_artifacts(target, package_dir=native.package)
    assert not target.exists()


def test_native_manifest_cannot_downgrade_default_sdk(native, tmp_path, monkeypatch):
    monkeypatch.setattr(sorust, "__file__", str(native.package / "__init__.py"))
    monkeypatch.setattr(sorust.ctypes, "CDLL", lambda *a: pytest.fail("native code must not load"))
    sorust._kernel.cache_clear()
    for operation in [sorust.verify_artifacts, sorust._kernel, sorust._compiled,
                      lambda: sorust.export_artifacts(tmp_path / "default-export")]:
        with pytest.raises(sorust.NativeArtifactError, match="dual-artifact"):
            operation()
    assert not (tmp_path / "default-export").exists()


@pytest.fixture
def old_reader(tmp_path):
    source = subprocess.check_output(['git', '-C', str(ROOT), 'show',
        '8de2464d896f336e3c27a35cc0001696416973ee:src/sorust/__init__.py'])
    path = tmp_path / "sorust_v20.py"
    path.write_bytes(source)
    spec = importlib.util.spec_from_file_location("sorust_v20", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_old_reader_refuses_native_schema_before_output(native, old_reader, tmp_path):
    with pytest.raises(old_reader.NativeArtifactError, match="unsupported manifest"):
        old_reader.verify_artifacts(native.package)
    with pytest.raises(old_reader.NativeArtifactError, match="unsupported manifest"):
        old_reader.export_artifacts(tmp_path / "old-export", package_dir=native.package)
    assert not (tmp_path / "old-export").exists()


@pytest.mark.parametrize("schema", ["sorust.artifacts/v1", "sorust.artifacts/v2"])
def test_old_and_new_readers_keep_dual_schemas(native, old_reader, tmp_path, schema):
    data = b"declared Python extension bytes"
    (native.package / "module.so").write_bytes(data)
    native.manifest.update(schema=schema)
    native.manifest["artifacts"].append(dict(kind="python-extension", path="module.so",
        sha256=hashlib.sha256(data).hexdigest()))
    if schema.endswith("v2"):
        native.manifest["resources"] = []
    native.pin()
    assert old_reader.verify_artifacts(native.package) == sorust.verify_artifacts(native.package)
    old_reader.export_artifacts(tmp_path / "old-export", package_dir=native.package)
    assert sorust.verify_artifacts(tmp_path / "old-export") == native.manifest


def test_real_native_wheel_install_metadata_export_and_c_abi(built, tmp_path):
    _, _, python, sdk_root = built
    manifest = sorust.verify_artifacts(sdk_root)
    wheel, descriptor, info = pilot.native_component_wheel(tmp_path, manifest, sdk_root)
    assert "py3-none-linux_x86_64" in wheel.name and info["pythonPayloadAbsent"]
    with zipfile.ZipFile(wheel) as archive:
        assert not any(name.endswith((".py", ".pyc", ".pyd")) for name in archive.namelist())
        assert sum(name.endswith(".so") for name in archive.namelist()) == 1
    run([python, "-I", "-m", "pip", "install", "--no-index", "--no-deps", wheel])
    destination = tmp_path / "installed-export"
    run([python, "-I", "-c", '''
import sys,json,importlib.metadata
from pathlib import Path
from sorust import backend,verify_artifacts,export_artifacts
spec=json.loads(sys.argv[1]);config={"rust-component":spec,"abi-version":1,"rust-library":"sorust_kernel"}
snapshot=backend._rust_component(config)
assert spec["package"] not in sys.modules
assert snapshot["provenance"]["distribution"]==spec["distribution"]
dist=importlib.metadata.distribution(spec["distribution"])
root=Path(dist.locate_file(spec["package"]))
assert not list(root.rglob("*.py"))
export_artifacts(sys.argv[2],package_dir=root)
assert verify_artifacts(sys.argv[2])["schema"]=="sorust.rust-component/v1"
''', json.dumps(descriptor), destination])
    assert sorust.verify_artifacts(destination) == info["manifest"]
    source = tmp_path / "client.c"
    source.write_text('''#include "sorust.h"
int main(void) { uint64_t n=0; const uint8_t text[]="one two three";
return !(sorust_abi_version()==1 && sorust_count_ascii_tokens_v1(text,sizeof(text)-1,&n)==0 && n==3); }
''')
    binary = tmp_path / "client"
    library = destination / "_native/libsorust_kernel.so"
    run(["cc", source, "-I", destination / "_native", library,
         "-Wl,-rpath," + str(library.parent), "-o", binary])
    run([binary])
