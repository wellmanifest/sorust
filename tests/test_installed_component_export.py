"""Export an installed atomic component using only the runtime SDK."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile

import pytest
import sorust
from sorust import backend
from sorust.__main__ import main
from test_build import ROOT, built, run
from test_nl_dsl_pilot import pilot
from test_prebuilt_component import donor
from test_rust_components import native


def arguments(spec):
    return {**{key.replace("-", "_"): value for key, value in spec.items()},
            "rust_library": "sorust_kernel"}


def cli_args(spec, destination):
    args = ["export-component", str(destination)]
    for key, value in arguments(spec).items():
        args.extend(["--" + key.replace("_", "-"), value])
    return args


def test_installed_export_preserves_raw_pin_without_import_or_load(native, tmp_path, monkeypatch):
    metadata = native.package / "sorust-artifacts.json"
    raw = (json.dumps(native.manifest, separators=(",", ":")) + "\n \n").encode()
    metadata.write_bytes(raw)
    native.spec["manifest-sha256"] = hashlib.sha256(raw).hexdigest()
    (native.package / "__init__.py").write_text('raise AssertionError("donor was imported")\n')
    monkeypatch.setattr(sorust.ctypes, "CDLL", lambda *a: pytest.fail("export loaded native code"))
    target = sorust.export_rust_component(tmp_path / "export", **arguments(native.spec))
    assert target == (tmp_path / "export").resolve()
    assert "kernel_pkg" not in sys.modules
    assert (target / metadata.name).read_bytes() == raw
    assert sorust.verify_artifacts(target) == native.manifest
    assert {f.relative_to(target).as_posix() for f in target.rglob("*") if f.is_file()} == {
        "sorust-artifacts.json", "_native/libsorust_kernel.so", "_native/sorust.h"}


@pytest.mark.parametrize("overrides,diagnostic", [
    ({"distribution": "other"}, "identity/version"),
    ({"version": "1.2.4"}, "identity/version"),
    ({"manifest_sha256": "0" * 64}, "pin mismatch"),
    ({"package": "../kernel"}, "requires distribution"),
    ({"rust_library": "another_kernel"}, "library identity"),
    ({"rust_library": "../kernel"}, "invalid Rust library"),
])
def test_installed_export_rejects_wrong_descriptor_before_output(native, tmp_path, overrides, diagnostic):
    target = tmp_path / "rejected"
    with pytest.raises(sorust.NativeArtifactError, match=diagnostic):
        sorust.export_rust_component(target, **(arguments(native.spec) | overrides))
    assert not target.exists()


@pytest.mark.parametrize("failure", ["unowned-manifest", "unowned-library", "linked-library", "drift"])
def test_installed_export_rejects_unowned_or_changed_payload(native, tmp_path, failure):
    relative = Path("_native/libsorust_kernel.so")
    if failure.startswith("unowned"):
        owned = Path("sorust-artifacts.json") if failure.endswith("manifest") else relative
        native.installed.files.remove(Path("kernel_pkg") / owned)
    elif failure == "linked-library":
        path = native.package / relative
        saved = path.with_name("saved.so")
        path.rename(saved)
        path.symlink_to(saved)
    else:
        (native.package / relative).write_bytes(b"changed")
    target = tmp_path / "rejected"
    with pytest.raises(sorust.NativeArtifactError):
        sorust.export_rust_component(target, **arguments(native.spec))
    assert not target.exists()


def test_installed_export_rejects_dual_component_without_changing_legacy_export(donor, tmp_path):
    target = tmp_path / "rejected"
    with pytest.raises(sorust.NativeArtifactError, match="Rust-only"):
        sorust.export_rust_component(target, **arguments(donor.spec))
    assert not target.exists()
    legacy = sorust.export_artifacts(tmp_path / "legacy", package_dir=donor.package)
    assert sorust.verify_artifacts(legacy) == donor.manifest


def test_installed_export_writes_snapshot_even_if_installation_changes_after_audit(native, tmp_path, monkeypatch):
    path = native.package / "_native/libsorust_kernel.so"
    original = path.read_bytes()
    snapshot = backend._rust_component

    def change_after_audit(config):
        component = snapshot(config)
        path.write_bytes(b"later installation")
        return component

    monkeypatch.setattr(backend, "_rust_component", change_after_audit)
    target = sorust.export_rust_component(tmp_path / "snapshot", **arguments(native.spec))
    assert path.read_bytes() != original
    assert (target / "_native/libsorust_kernel.so").read_bytes() == original
    assert sorust.verify_artifacts(target) == native.manifest


def test_installed_export_never_reuses_existing_destination(native, tmp_path):
    existing = tmp_path / "existing"
    existing.mkdir()
    marker = existing / "previous"
    marker.write_bytes(b"keep")
    linked = tmp_path / "linked"
    linked.symlink_to(existing, target_is_directory=True)
    for target in [existing, linked]:
        with pytest.raises(FileExistsError):
            sorust.export_rust_component(target, **arguments(native.spec))
    assert list(existing.iterdir()) == [marker]
    assert marker.read_bytes() == b"keep"


def test_export_component_cli_rejects_bad_pin(native, tmp_path, capsys):
    target = tmp_path / "rejected"
    with pytest.raises(SystemExit) as e:
        main(cli_args(native.spec | {"manifest-sha256": "0" * 64}, target))
    assert e.value.code == 1
    output = capsys.readouterr()
    assert "pin mismatch" in output.err and not output.out
    assert not target.exists()


def test_installed_native_wheel_api_and_cli_without_build_dependencies(built, tmp_path):
    _, _, python, sdk_root = built
    wheel, spec, info = pilot.native_component_wheel(tmp_path, sorust.verify_artifacts(sdk_root), sdk_root)
    run([python, "-I", "-m", "pip", "install", "--no-index", "--no-deps", wheel])
    no_tools = tmp_path / "no-tools"
    no_tools.mkdir()
    environment = dict(os.environ, PATH=str(no_tools))
    environment.pop("PYTHONPATH", None)

    def runtime(*args):
        result = subprocess.run([python, "-I", *args], cwd=ROOT, env=environment,
                                capture_output=True, text=True, timeout=60)
        assert result.returncode == 0, result.stdout + result.stderr
        return result.stdout.strip()

    api = tmp_path / "api"
    cli = tmp_path / "cli"
    runtime("-c", '''import importlib.util,json,shutil,sys
from sorust import export_rust_component
assert all(importlib.util.find_spec(n) is None for n in ["Cython","setuptools","wheel","build"])
assert all(shutil.which(n) is None for n in ["cargo","rustc","cc","gcc"])
args=json.loads(sys.argv[1]);export_rust_component(sys.argv[2],**args)
assert args["package"] not in sys.modules
''', json.dumps(arguments(spec)), str(api))
    assert runtime("-m", "sorust", *cli_args(spec, cli)) == str(cli.resolve())
    with zipfile.ZipFile(wheel) as archive:
        for target in [api, cli]:
            assert sorust.verify_artifacts(target) == info["manifest"]
            for name in ["sorust-artifacts.json", "_native/libsorust_kernel.so", "_native/sorust.h"]:
                assert (target / name).read_bytes() == archive.read(spec["package"] + "/" + name)
