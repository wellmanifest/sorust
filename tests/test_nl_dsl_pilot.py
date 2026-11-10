"""Guards for the optional offline real-consumer developer pilot."""
import copy
import importlib.util
import json
import os
import shutil
from pathlib import Path
import subprocess
import zipfile

import pytest

spec = importlib.util.spec_from_file_location("nl_pilot", Path(__file__).with_name("benchmark_nl_dsl_pilot.py"))
pilot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pilot)


@pytest.fixture
def committed_source(tmp_path):
    repo = tmp_path / "consumer"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    source = repo / "source.py"
    source.write_bytes(b"committed source\n")
    subprocess.run(["git", "add", "source.py"], cwd=repo, check=True)
    subprocess.run(["git", "-c", "user.name=Pilot Test", "-c", "user.email=pilot@example.invalid",
                    "commit", "-qm", "fixture"], cwd=repo, check=True)
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    return repo, source, revision


def test_snapshot_uses_commit_instead_of_dirty_worktree(committed_source):
    repo, source, revision = committed_source
    source.write_bytes(b"modified working tree\n")
    assert pilot.snapshot(repo, revision, ["source.py"]) == {"source.py": b"committed source\n"}
    assert source.read_bytes() == b"modified working tree\n"


@pytest.mark.parametrize("revision", ["main", "HEAD", "a" * 39, "A" * 40])
def test_snapshot_rejects_mutable_or_malformed_revision(tmp_path, revision, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Git must not run for a malformed pin")
    monkeypatch.setattr(pilot.subprocess, "check_output", forbidden)
    with pytest.raises(ValueError, match="40-hex"):
        pilot.snapshot(tmp_path, revision)


def test_snapshot_rejects_blob_pin(committed_source):
    repo, _, revision = committed_source
    blob = subprocess.check_output(["git", "rev-parse", revision + ":source.py"], cwd=repo, text=True).strip()
    with pytest.raises(ValueError, match="commit"):
        pilot.snapshot(repo, blob, ["source.py"])


def test_output_refuses_reuse_without_erasing_previous_data(tmp_path):
    root = tmp_path.resolve()
    output = pilot.new_output(root, Path(".subactor/cache/pilot"))
    marker = output / "evidence.json"
    marker.write_bytes(b"previous evidence")
    with pytest.raises(FileExistsError):
        pilot.new_output(root, output)
    assert marker.read_bytes() == b"previous evidence"


@pytest.mark.parametrize("relative", ["outside", ".subactor/cache/../outside"])
def test_output_confined_to_private_cache(tmp_path, relative):
    with pytest.raises(ValueError, match=".subactor/cache"):
        pilot.new_output(tmp_path, Path(relative))
    assert not (tmp_path / "outside").exists()


def test_output_rejects_linked_parent(tmp_path):
    cache = tmp_path / ".subactor/cache"
    cache.mkdir(parents=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    (cache / "linked").symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError, match="symlinks"):
        pilot.new_output(tmp_path, cache / "linked/pilot")
    assert not (outside / "pilot").exists()


def test_wheel_rejects_stale_backend(tmp_path):
    wheel = tmp_path / "stale.whl"
    with zipfile.ZipFile(wheel, "w") as archive:
        archive.writestr("sorust/__init__.py", (pilot.ROOT / "src/sorust/__init__.py").read_bytes())
        archive.writestr("sorust/backend.py", "stale backend")
    with pytest.raises(ValueError, match="match this checkout"):
        pilot.check_wheel(wheel, pilot.ROOT, {})


@pytest.mark.parametrize("mismatch", ["manifest", "artifact"])
def test_wheel_binds_reused_native_artifacts(tmp_path, mismatch):
    wheel = tmp_path / "mismatch.whl"
    expected = {"artifacts": [{"path": "_native/kernel.so", "sha256": pilot.digest(b"expected")}],
                "headers": []}
    supplied = copy.deepcopy(expected)
    if mismatch == "manifest":
        supplied["artifacts"][0]["sha256"] = pilot.digest(b"other")
    with zipfile.ZipFile(wheel, "w") as archive:
        for name in ["__init__.py", "backend.py"]:
            archive.writestr("sorust/" + name, (pilot.ROOT / "src/sorust" / name).read_bytes())
        archive.writestr("sorust/sorust-artifacts.json", json.dumps(supplied))
        archive.writestr("sorust/_native/kernel.so", b"other")
    diagnostic = "artifact manifest" if mismatch == "manifest" else "native artifact bytes"
    with pytest.raises(ValueError, match=diagnostic):
        pilot.check_wheel(wheel, pilot.ROOT, expected)


@pytest.mark.parametrize("mode", ["wheel", "exported"])
def test_comparison_rejects_behavior_drift(mode):
    result = {x: {"observations": {"parse": [{"entity": "ticket"}]}}
              for x in ["source", "wheel", "exported"]}
    result[mode]["observations"]["parse"][0]["entity"] = "other"
    with pytest.raises(ValueError, match=mode):
        pilot.compare(result)


def test_comparison_excludes_timing_noise():
    result = {x: {"observations": {"values": [1, 2]}, "measurements": {"time": n}}
              for n, x in enumerate(["source", "wheel", "exported"])}
    before = copy.deepcopy(result)
    assert len(pilot.compare(result)) == 64
    assert result == before


def test_conformance_propagates_failures(tmp_path):
    source = tmp_path / "conformance.py"
    source.write_text('def test_broken():\n    raise AssertionError("consumer regression")\n')
    with pytest.raises(AssertionError, match="consumer regression"):
        pilot.conformance(source)


@pytest.mark.parametrize("source", ["", "def test_fixture(value):\n    pass\n"])
def test_conformance_never_silently_skips_unknown_tests(tmp_path, source):
    path = tmp_path / "conformance.py"
    path.write_text(source)
    with pytest.raises(ValueError, match="argument-free"):
        pilot.conformance(path)


@pytest.fixture
def wheel_inputs(tmp_path):
    source = tmp_path / "input wheels"
    source.mkdir()
    sdk = tmp_path / "sorust-0.1.0-cp313-cp313-linux_x86_64.whl"
    sdk.write_bytes(b"bound sdk snapshot")
    (source / sdk.name).write_bytes(sdk.read_bytes())
    dependency = source / "dependency-1.0-py3-none-any.whl"
    dependency.write_bytes(b"dependency snapshot")
    return source, sdk, dependency


def test_wheelhouse_freezes_exact_inputs_and_records_hashes(tmp_path, wheel_inputs):
    source, sdk, dependency = wheel_inputs
    target = tmp_path / "snapshot"
    inventory = pilot.snapshot_wheelhouse(source, target, sdk)
    assert inventory == [{"file": p.name, "sha256": pilot.digest(p.read_bytes())}
                         for p in sorted(source.iterdir())]
    dependency.write_bytes(b"changed after snapshot")
    assert (target / dependency.name).read_bytes() == b"dependency snapshot"
    assert (target / sdk.name).read_bytes() == sdk.read_bytes()


@pytest.mark.parametrize("case", ["missing", "file", "root-link", "parent-link", "dotdot"])
def test_wheelhouse_rejects_unsafe_directory_before_output(tmp_path, wheel_inputs, case):
    source, sdk, _ = wheel_inputs
    if case == "missing":
        source = tmp_path / "missing"
    elif case == "file":
        source = sdk
    elif case == "root-link":
        link = tmp_path / "linked"
        link.symlink_to(source, target_is_directory=True)
        source = link
    elif case == "parent-link":
        link = tmp_path / "parent"
        link.symlink_to(tmp_path, target_is_directory=True)
        source = link / source.name
    else:
        source = source / ".." / source.name
    target = tmp_path / "snapshot"
    with pytest.raises(ValueError, match="regular directory"):
        pilot.snapshot_wheelhouse(source, target, sdk)
    assert not target.exists()


@pytest.mark.parametrize("case", ["empty", "sdist", "directory", "linked-wheel", "missing-sdk", "stale-sdk"])
def test_wheelhouse_rejects_incomplete_or_unsafe_inputs(tmp_path, wheel_inputs, case):
    source, sdk, dependency = wheel_inputs
    if case == "empty":
        (source / sdk.name).unlink()
        dependency.unlink()
    elif case == "sdist":
        (source / "other.tar.gz").write_bytes(b"not a binary dependency")
    elif case == "directory":
        (source / "nested.whl").mkdir()
    elif case == "linked-wheel":
        dependency.unlink()
        dependency.symlink_to(sdk)
    elif case == "missing-sdk":
        (source / sdk.name).unlink()
    else:
        (source / sdk.name).write_bytes(b"stale SDK")
    target = tmp_path / "snapshot"
    with pytest.raises(ValueError, match="regular wheel|exact current"):
        pilot.snapshot_wheelhouse(source, target, sdk)
    assert not target.exists()


def test_wheelhouse_preserves_existing_snapshot(tmp_path, wheel_inputs):
    source, sdk, _ = wheel_inputs
    target = tmp_path / "snapshot"
    target.mkdir()
    marker = target / "receipt"
    marker.write_bytes(b"earlier result")
    with pytest.raises(FileExistsError):
        pilot.snapshot_wheelhouse(source, target, sdk)
    assert marker.read_bytes() == b"earlier result" and list(target.iterdir()) == [marker]


def test_isolated_frontend_refuses_missing_local_build_dependency(tmp_path, wheel_inputs):
    source, sdk, _ = wheel_inputs
    run = tmp_path / "run"
    run.mkdir()
    environment = dict(os.environ, PIP_INDEX_URL="https://example.invalid/forbidden-index",
                       PIP_FIND_LINKS="https://example.invalid/forbidden-links")
    with pytest.raises(RuntimeError, match="frontend-install.log"):
        pilot.isolated_frontend(run, source, sdk, environment)
    log = (run / "frontend-install.log").read_text()
    assert "No matching distribution found for build" in log
    assert "example.invalid" not in log
    result = subprocess.run([run / "builder/bin/python", "-I", "-c",
        'import importlib.util; assert all(importlib.util.find_spec(n) is None for n in ["build", "sorust", "Cython", "setuptools"])'],
        text=True, capture_output=True, timeout=30)
    assert result.returncode == 0, result.stdout + result.stderr


def test_isolated_pilot_requires_prebuilt_mode_before_reading_inputs(monkeypatch, tmp_path):
    from argparse import Namespace
    monkeypatch.setattr(pilot, "snapshot", lambda *a: pytest.fail("consumer input must not be read"))
    with pytest.raises(ValueError, match="requires --prebuilt-rust"):
        pilot.pilot(Namespace(build_wheelhouse=tmp_path, prebuilt_rust=False))


def test_c_build_path_excludes_rust_and_preserves_c_compiler(tmp_path):
    tools = pilot.c_build_path(tmp_path, dict(os.environ))
    assert shutil.which("rustc", path=str(tools)) is None
    assert shutil.which("cargo", path=str(tools)) is None
    compiler = shutil.which("cc", path=str(tools))
    assert compiler and Path(compiler).samefile(shutil.which("cc"))


def test_c_build_path_rejects_rust_selected_as_c_compiler(tmp_path):
    selected = tmp_path / "outside"
    selected.mkdir()
    rust = selected / "rustc"
    rust.write_text("#!/bin/sh\nexit 97\n")
    rust.chmod(0o755)
    with pytest.raises(ValueError, match="must not select"):
        pilot.c_build_path(tmp_path, dict(os.environ, CC=str(rust)))


def test_wheelhouse_includes_generated_component_snapshot(tmp_path, wheel_inputs):
    source, sdk, _ = wheel_inputs
    extra = tmp_path / "component-1.0-py3-none-linux_x86_64.whl"
    extra.write_bytes(b"generated native wheel")
    target = tmp_path / "snapshot"
    inventory = pilot.snapshot_wheelhouse(source, target, sdk, [extra])
    assert inventory[-1] == {"file": extra.name, "sha256": pilot.digest(extra.read_bytes())}
    extra.write_bytes(b"changed later")
    assert (target / extra.name).read_bytes() == b"generated native wheel"


@pytest.mark.parametrize("case", ["missing", "linked", "collision"])
def test_generated_component_cannot_replace_or_escape_inputs(tmp_path, wheel_inputs, case):
    source, sdk, dependency = wheel_inputs
    extra = tmp_path / "extra.whl"
    if case == "linked":
        extra.symlink_to(dependency)
    elif case == "collision":
        extra = dependency
    with pytest.raises(ValueError, match="must not replace"):
        pilot.snapshot_wheelhouse(source, tmp_path / "snapshot", sdk, [extra])
    assert not (tmp_path / "snapshot").exists()
    assert (source / sdk.name).read_bytes() == sdk.read_bytes()


@pytest.mark.parametrize("prebuilt", [False, True])
def test_native_component_pilot_requires_isolated_prebuilt_mode(monkeypatch, prebuilt):
    from argparse import Namespace
    monkeypatch.setattr(pilot, "snapshot", lambda *a: pytest.fail("inputs must not be read"))
    with pytest.raises(ValueError, match="native-only-component requires"):
        pilot.pilot(Namespace(build_wheelhouse=None, prebuilt_rust=prebuilt, native_only_component=True))
