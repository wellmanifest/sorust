"""Declared data resources survive build/export and fail closed on drift."""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import venv
import zipfile

import pytest
import sorust
from sorust.backend import configuration
from test_build import ROOT, built, external_project, run


def declare(project, resources):
    path = project / "pyproject.toml"
    path.write_text(path.read_text().replace("abi-version = 1\n",
                    "abi-version = 1\nresources = " + json.dumps(resources) + "\n", 1))


@pytest.mark.parametrize("resources", [
    "settings.json", 42, [42], [True], ["settings.json", "settings.json"],
    [""], ["."], ["../settings.json"], ["/settings.json"], ["./settings.json"],
    ["data//settings.json"], ["data/../settings.json"], ["C:/settings.json"],
    ["data\\settings.json"], ["*.json"], ["sorust-artifacts.json"],
    ["sorust-artifacts.json/child.json"], ["_native/data.json"], ["_compat.py"], ["library.so"],
])
def test_resource_configuration_rejects_unsafe_values(tmp_path, resources):
    project, package, _ = external_project(tmp_path)
    (package / "settings.json").write_text('{}')
    declare(project, resources)
    with pytest.raises(ValueError, match="resource"):
        configuration(project)


@pytest.mark.parametrize("case", ["missing", "directory", "link-inside", "link-outside", "parent-link"])
def test_resource_configuration_requires_regular_unlinked_file(tmp_path, case):
    project, package, _ = external_project(tmp_path)
    declare(project, ["data/settings.json"])
    directory = package / "data"
    directory.mkdir()
    path = directory / "settings.json"
    if case == "directory":
        path.mkdir()
    elif case.startswith("link-"):
        saved = (package if case == "link-inside" else tmp_path) / "saved.json"
        saved.write_text('{}')
        path.symlink_to(saved)
    elif case == "parent-link":
        directory.rmdir()
        actual = package / "actual"
        actual.mkdir()
        (actual / "settings.json").write_text('{}')
        directory.symlink_to(actual, target_is_directory=True)
    with pytest.raises(ValueError, match="resource"):
        configuration(project)


def test_resource_missing_fails_pep517_before_compilers(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    for name in ["pyproject.toml", "README.md", "VERSION", "MANIFEST.in"]:
        shutil.copyfile(ROOT / name, project / name)
    for name in ["src", "crates", "include"]:
        shutil.copytree(ROOT / name, project / name,
                        ignore=shutil.ignore_patterns("__pycache__", "*.egg-info", "target"))
    declare(project, ["settings.json"])
    environment = dict(os.environ)
    environment.pop("PYTHONPATH", None)
    output = tmp_path / "dist"
    result = subprocess.run([sys.executable, "-I", "-m", "build", "--sdist", "--no-isolation",
                             "--outdir", str(output), str(project)], cwd=project, env=environment,
                            text=True, capture_output=True, timeout=180)
    assert result.returncode != 0 and "missing or unsafe resource" in result.stdout + result.stderr
    assert not (project / "build").exists() and not list(output.glob("*.tar.gz"))


@pytest.fixture
def resource_package(tmp_path):
    package = tmp_path / "package"
    files = {"module.so": b"test-only extension bytes", "_native/kernel.so": b"test-only Rust bytes",
             "data/settings.json": b'{"factor":2}'}
    for name, data in files.items():
        path = package / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    entry = lambda name: {"path": name, "sha256": hashlib.sha256(files[name]).hexdigest()}
    manifest = {"schema": "sorust.artifacts/v2", "abi_version": 1,
                "artifacts": [dict(kind="python-extension", **entry("module.so")),
                              dict(kind="rust-cdylib", **entry("_native/kernel.so"))],
                "resources": [entry("data/settings.json")]}
    (package / "sorust-artifacts.json").write_text(json.dumps(manifest))
    return package, manifest


@pytest.mark.parametrize("schema", ["sorust.artifacts/v1", "sorust.artifacts/v2"])
def test_resource_manifest_legacy_and_new_export_contract(resource_package, tmp_path, schema):
    package, manifest = resource_package
    manifest["schema"] = schema
    if schema.endswith("v1"):
        manifest.pop("resources")
    (package / "sorust-artifacts.json").write_text(json.dumps(manifest))
    assert sorust.verify_artifacts(package) == manifest
    exported = sorust.export_artifacts(tmp_path / "exported", package_dir=package)
    assert sorust.verify_artifacts(exported) == manifest
    assert (exported / "data/settings.json").exists() == schema.endswith("v2")


@pytest.mark.parametrize("case", ["missing", "changed", "leaf-link", "parent-link"])
def test_resource_manifest_drift_rejected_before_export(resource_package, tmp_path, case):
    package, _ = resource_package
    path = package / "data/settings.json"
    if case == "missing":
        path.unlink()
    elif case == "changed":
        path.write_text('{"factor":99}')
    elif case == "leaf-link":
        saved = package / "saved.json"
        path.rename(saved)
        path.symlink_to(saved)
    else:
        (package / "data").rename(package / "actual")
        (package / "data").symlink_to(package / "actual", target_is_directory=True)
    with pytest.raises(sorust.NativeArtifactError):
        sorust.verify_artifacts(package)
    destination = tmp_path / "refused"
    with pytest.raises(sorust.NativeArtifactError):
        sorust.export_artifacts(destination, package_dir=package)
    assert not destination.exists()


@pytest.mark.parametrize("case", ["v1-resources", "missing-list", "wrong-list", "wrong-entry", "duplicate",
                                  "header-collision", "escape", "alias", "reserved"])
def test_resource_manifest_rejects_inconsistent_declarations(resource_package, case):
    package, manifest = resource_package
    if case == "v1-resources":
        manifest["schema"] = "sorust.artifacts/v1"
    elif case == "missing-list":
        manifest.pop("resources")
    elif case == "wrong-list":
        manifest["resources"] = {}
    elif case == "wrong-entry":
        manifest["resources"] = [None]
    elif case == "duplicate":
        manifest["resources"] *= 2
    elif case == "header-collision":
        manifest["headers"] = copy.deepcopy(manifest["resources"])
    else:
        manifest["resources"][0]["path"] = {"escape": "../settings.json", "alias": "./data/settings.json",
                                              "reserved": "sorust-artifacts.json"}[case]
    (package / "sorust-artifacts.json").write_text(json.dumps(manifest))
    with pytest.raises(sorust.NativeArtifactError):
        sorust.verify_artifacts(package)


def test_resource_export_rechecks_snapshot(resource_package, tmp_path, monkeypatch):
    package, _ = resource_package
    original = sorust.verify_artifacts

    def change_after_verification(root):
        manifest = original(root)
        path = root / "data/settings.json"
        path.write_bytes(path.read_bytes() + b" ")
        return manifest

    monkeypatch.setattr(sorust, "verify_artifacts", change_after_verification)
    destination = tmp_path / "refused"
    with pytest.raises(sorust.NativeArtifactError, match="changed before export"):
        sorust.export_artifacts(destination, package_dir=package)
    assert not destination.exists()


def test_resource_sdist_rebuild_and_standalone_compiled_import(built, tmp_path):
    _, sorust_wheel, python, _ = built
    run([sys.executable, "-I", "-m", "pip", "install", "--no-deps", "--force-reinstall", sorust_wheel])
    project, package, _ = external_project(tmp_path, "initializers")
    declare(project, ["settings.json", "nested/config.bin"])
    config = project / "pyproject.toml"
    config.write_text(config.read_text() + '\n[tool.setuptools]\ninclude-package-data = false\n')
    for relative, function, filename in [("_compat.py", "double", "settings.json"),
                                         ("nested/_fast.py", "triple", "config.bin")]:
        (package / relative).write_text('from pathlib import Path\nimport json\n'
            f'def {function}(value):\n    return value * json.loads(Path(__file__).with_name("{filename}").read_bytes())["factor"]\n')
    (package / "nested/config.bin").write_bytes(b'{"factor":3}')
    observations = []
    minimal = tmp_path / "minimal"
    venv.EnvBuilder(with_pip=False, symlinks=False).create(minimal)
    for factor in [2, 5]:
        (package / "settings.json").write_text(json.dumps({"factor": factor}))
        output = tmp_path / f"dist-{factor}"
        run([sys.executable, "-I", "-m", "build", "--no-isolation", "--outdir", output, project])
        with tarfile.open(next(output.glob("*.tar.gz"))) as archive:
            for relative in ["settings.json", "nested/config.bin"]:
                member = next(x for x in archive.getmembers() if x.name.endswith("/src/nl_atomic_example/" + relative))
                assert archive.extractfile(member).read() == (package / relative).read_bytes()
        wheel = next(output.glob("*.whl"))
        with zipfile.ZipFile(wheel) as archive:
            manifest = json.loads(archive.read("nl_atomic_example/sorust-artifacts.json"))
            assert manifest["schema"] == "sorust.artifacts/v2" and manifest["abi_version"] == 1
            assert {x["path"] for x in manifest["resources"]} == {"settings.json", "nested/config.bin"}
            for item in manifest["artifacts"] + manifest["headers"] + manifest["resources"]:
                assert hashlib.sha256(archive.read("nl_atomic_example/" + item["path"])).hexdigest() == item["sha256"]
        observations.append(manifest["source_sha256"])
        run([python, "-I", "-m", "pip", "install", "--no-deps", "--force-reinstall", wheel])
        exported = tmp_path / f"export-{factor}/nl_atomic_example"
        exported.parent.mkdir()
        run([python, "-I", "-c", '''
from pathlib import Path
import sys, sorust, nl_atomic_example
source = Path(nl_atomic_example.__file__).parent
manifest = sorust.verify_artifacts(source)
destination = sorust.export_artifacts(sys.argv[1], package_dir=source)
assert sorust.verify_artifacts(destination) == manifest
''', exported])
        run([minimal / "bin/python", "-I", "-c", '''
import importlib.machinery, importlib.util, sys
sys.path.insert(0, sys.argv[1])
assert importlib.util.find_spec("sorust") is None
assert importlib.util.find_spec("Cython") is None
import nl_atomic_example as module
assert isinstance(module.__loader__, importlib.machinery.ExtensionFileLoader)
assert module.double(7) == int(sys.argv[2]) * 7
assert module.triple(7) == 21
''', exported.parent, factor])
    assert observations[0] != observations[1], "resource-only change missing from source fingerprint"
