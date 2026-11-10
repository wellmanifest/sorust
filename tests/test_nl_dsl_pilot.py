"""Guards for the optional offline real-consumer developer pilot."""
import copy
import importlib.util
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
        pilot.check_wheel(wheel, pilot.ROOT)


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
