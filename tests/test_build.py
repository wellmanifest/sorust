"""Real build/install/link tests; all compiler and runtime processes are exercised."""
import json
import hashlib
import ctypes
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import venv
import zipfile

import pytest

ROOT = Path(__file__).resolve().parents[1]


def run(args, *, cwd=ROOT):
    environment = dict(os.environ)
    environment.pop("PYTHONPATH", None)
    result = subprocess.run([str(x) for x in args], cwd=cwd, text=True,
                            capture_output=True, timeout=180, env=environment)
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    output = tmp_path_factory.mktemp("built")
    run([sys.executable, "-m", "build", "--no-isolation", "--outdir", output])
    wheel = next(output.glob("*.whl"))
    assert "none-any" not in wheel.name
    env = output / "runtime"
    venv.EnvBuilder(with_pip=True, symlinks=False).create(env)
    python = env / "bin/python"
    run([python, "-I", "-m", "pip", "install", "--no-deps", wheel])
    package = Path(run([python, "-I", "-c",
                        "import sorust; from pathlib import Path; print(Path(sorust.__file__).parent)"]).strip())
    return output, wheel, python, package


def test_installed_wheel_parity_and_abi(built):
    _, wheel, python, package = built
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        assert any(x.startswith("sorust/_compat.") and x.endswith(".so") for x in names)
        assert any(x.startswith("sorust/_native/") and x.endswith(".so") for x in names)
        assert "sorust/_compat.py" not in names
        assert "sorust/_native/sorust.h" in names
    run([python, "-I", "-c", r'''
import ctypes, importlib.machinery, random, re
import sorust
from sorust import _compat
assert any(_compat.__file__.endswith(x) for x in importlib.machinery.EXTENSION_SUFFIXES)
rng = random.Random(123)
values = [b"", b"\x00\xff", bytes(range(256)), "zażółć gęślą".encode()]
values += [rng.randbytes(rng.randrange(4096)) for _ in range(300)]
for value in values:
    expected = len(re.findall(rb"[^\x09-\x0d\x20]+", value))
    assert sorust.count_ascii_tokens(value) == expected
    assert sorust.count_ascii_tokens(value, backend="compiled-python") == expected
library, function = sorust._kernel()
output = ctypes.c_uint64(99)
assert library.sorust_abi_version() == 1
assert function(None, 1, ctypes.byref(output)) == 1 and output.value == 99
assert function(None, 0, ctypes.byref(output)) == 0 and output.value == 0
for backend in ("rust", "compiled-python"):
    try: sorust.count_ascii_tokens("bad", backend=backend)
    except TypeError: pass
    else: raise AssertionError("accepted non-bytes")
try: sorust.count_ascii_tokens(b"a", backend="unknown")
except ValueError: pass
else: raise AssertionError("accepted unknown backend")
'''])
    assert package.is_dir()


def test_manifest_integrity_and_abi_rejections(built, tmp_path):
    _, _, python, package = built
    clone = tmp_path / "sorust"
    shutil.copytree(package, clone)
    manifest_path = clone / "sorust-artifacts.json"
    manifest = json.loads(manifest_path.read_text())
    binary = clone / manifest["artifacts"][1]["path"]
    binary.write_bytes(binary.read_bytes() + b"corruption")
    run([python, "-I", "-c", '''
import sys, sorust
try: sorust.verify_artifacts(sys.argv[1])
except sorust.NativeArtifactError: pass
else: raise AssertionError("corrupt binary accepted")
''', clone])
    manifest["abi_version"] = 2
    manifest_path.write_text(json.dumps(manifest))
    run([python, "-I", "-c", '''
import sys, sorust
try: sorust.verify_artifacts(sys.argv[1])
except sorust.NativeArtifactError: pass
else: raise AssertionError("incompatible ABI accepted")
''', clone])
    source = tmp_path / "wrong_abi.c"
    source.write_text("unsigned int sorust_abi_version(void) { return 2; }\n")
    run(["cc", "-shared", "-fPIC", source, "-o", binary])
    manifest["abi_version"] = 1
    manifest["artifacts"][1]["sha256"] = hashlib.sha256(binary.read_bytes()).hexdigest()
    manifest_path.write_text(json.dumps(manifest))
    run([python, "-I", "-c", '''
import sys
sys.path.insert(0, sys.argv[1])
import sorust
try: sorust.count_ascii_tokens(b"one two")
except sorust.NativeArtifactError as error: assert "ABI" in str(error)
else: raise AssertionError("loaded incompatible library accepted")
''', tmp_path])


def test_sdist_has_native_sources(built):
    output, _, _, _ = built
    with tarfile.open(next(output.glob("*.tar.gz"))) as archive:
        names = archive.getnames()
        assert not any("/build/" in name or "/target/" in name for name in names)
        for suffix in ("crates/sorust-kernel/Cargo.lock", "crates/sorust-kernel/src/lib.rs",
                       "include/sorust.h", "src/sorust/backend.py"):
            assert any(name.endswith(suffix) for name in names)


@pytest.mark.parametrize("case", ["unlisted", "source", "missing", "preloaded"])
def test_compiled_import_requires_manifest_bound_native_module(built, tmp_path, case):
    _, _, python, package = built
    clone = tmp_path / "sorust"
    shutil.copytree(package, clone)
    manifest_path = clone / "sorust-artifacts.json"
    manifest = json.loads(manifest_path.read_text())
    entry = next(item for item in manifest["artifacts"] if item["kind"] == "python-extension")
    original = clone / entry["path"]
    listed_copy = clone / "listed_copy.so"
    shutil.copyfile(original, listed_copy)
    entry["path"] = listed_copy.name
    manifest_path.write_text(json.dumps(manifest))
    marker = tmp_path / "uncompiled-source-ran"
    if case in {"source", "missing"}:
        original.unlink()
    if case == "source":
        (clone / "_compat.py").write_text(
            f"from pathlib import Path\nPath({str(marker)!r}).write_text('executed')\n"
            "def count_ascii_tokens(data):\n    return 2\n")
    run([python, "-I", "-c", '''
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import sorust
sorust.verify_artifacts()
if sys.argv[2] == "preloaded":
    from sorust import _compat
try:
    sorust.count_ascii_tokens(b"one two", backend="compiled-python")
except sorust.NativeArtifactError:
    pass
else:
    raise AssertionError("unlisted compiled module accepted")
assert not Path(sys.argv[3]).exists(), "uncompiled Python executed before rejection"
if sys.argv[2] != "preloaded":
    assert "sorust._compat" not in sys.modules, "unverified module imported before rejection"
''', tmp_path, case, marker])


def test_c_consumer_links_installed_binary(built, tmp_path):
    _, _, _, package = built
    manifest = json.loads((package / "sorust-artifacts.json").read_text())
    library = package / next(x["path"] for x in manifest["artifacts"] if x["kind"] == "rust-cdylib")
    source = tmp_path / "consumer.c"
    source.write_text('''#include "sorust.h"
int main(void) { uint64_t n=0; const uint8_t text[]="one two\\tthree";
return !(sorust_abi_version()==1 && sorust_count_ascii_tokens_v1(text, sizeof(text)-1, &n)==0 && n==3); }
''')
    binary = tmp_path / "consumer"
    run(["cc", source, "-I", package / "_native", library,
         "-Wl,-rpath," + str(library.parent), "-o", binary])
    run([binary])


def test_rust_bytes_subclass_uses_buffer_length(monkeypatch):
    import sorust

    class MisleadingLength(bytes):
        def __len__(self):
            return 1024

    def capture(data, length, output):
        assert length == memoryview(data).nbytes == 7
        ctypes.cast(output, ctypes.POINTER(ctypes.c_uint64))[0] = 2
        return 0

    monkeypatch.setattr(sorust, "_kernel", lambda: (None, capture))
    assert sorust.count_ascii_tokens(MisleadingLength(b"one two")) == 2


def test_rust_bytes_passthrough_avoids_copy(monkeypatch):
    import sorust
    payload = b"one two"

    def capture(data, length, output):
        assert data is payload and length == 7
        ctypes.cast(output, ctypes.POINTER(ctypes.c_uint64))[0] = 2
        return 0

    monkeypatch.setattr(sorust, "_kernel", lambda: (None, capture))
    assert sorust.count_ascii_tokens(payload) == 2


@pytest.mark.parametrize("case", ["plain", "length", "iteration", "bytes", "combined"])
def test_installed_bytes_subclass_parity(built, case):
    _, _, python, _ = built
    run([python, "-I", "-c", '''
import importlib.util
import sys
import sorust
spec = importlib.util.spec_from_file_location("reference", sys.argv[1])
reference = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)
class Plain(bytes): pass
class Length(bytes):
    def __len__(self): return 0
class Iteration(bytes):
    def __iter__(self): return iter([32])
class BytesHook(bytes):
    def __bytes__(self): return b"wrong wrong wrong"
class Combined(Length, Iteration, BytesHook): pass
classes = {"plain": Plain, "length": Length, "iteration": Iteration,
           "bytes": BytesHook, "combined": Combined}
payload = classes[sys.argv[2]](b"one two")
assert reference.count_ascii_tokens(payload) == 2
for backend in ("rust", "compiled-python"):
    assert sorust.count_ascii_tokens(payload, backend=backend) == 2
''', ROOT / "src/sorust/_compat.py", case])


def test_rust_consumer_reuses_rlib(tmp_path):
    target = tmp_path / "target"
    run(["cargo", "test", "--locked", "--offline", "--manifest-path",
         ROOT / "crates/sorust-kernel/Cargo.toml", "--target-dir", target])
    run(["cargo", "build", "--release", "--locked", "--offline", "--manifest-path",
         ROOT / "crates/sorust-kernel/Cargo.toml", "--target-dir", target])
    source = tmp_path / "consumer.rs"
    source.write_text('fn main() { assert_eq!(sorust_kernel::count_ascii_tokens(b"one two"), 2); }')
    binary = tmp_path / "consumer"
    run(["rustc", source, "--edition=2021", "-Cpanic=abort", "--extern",
         "sorust_kernel=" + str(target / "release/libsorust_kernel.rlib"), "-o", binary])
    run([binary])


def test_python_consumer_shares_installed_kernel(built, tmp_path):
    output, _, python, _ = built
    project = tmp_path / "consumer"
    package = project / "src/nl_sorust_example"
    package.mkdir(parents=True)
    (project / "pyproject.toml").write_text('''[build-system]
requires = ["setuptools>=77", "wheel>=0.45"]
build-backend = "setuptools.build_meta"
[project]
name = "nl-sorust-example"
version = "0.1.0"
dependencies = ["sorust>=0.1.0,<0.2"]
[tool.setuptools.packages.find]
where = ["src"]
''')
    (package / "__init__.py").write_text('''from sorust import count_ascii_tokens
def count_prompt_tokens(prompt: str) -> int:
    return count_ascii_tokens(prompt.encode("utf-8"))
''')
    consumer_dist = output / "consumer-dist"
    run([sys.executable, "-I", "-m", "build", "--wheel", "--no-isolation",
         "--outdir", consumer_dist, project])
    run([python, "-I", "-m", "pip", "install", "--no-deps", next(consumer_dist.glob("*.whl"))])
    run([python, "-I", "-c", 'from nl_sorust_example import count_prompt_tokens; assert count_prompt_tokens("one two") == 2'])


def test_external_consumer_build_backend(built, tmp_path):
    _, wheel, python, _ = built
    run([sys.executable, "-I", "-m", "pip", "install", "--no-deps", "--force-reinstall", wheel])
    project = tmp_path / "external"
    package = project / "src/nl_atomic_example"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("")
    (package / "_compat.py").write_text("def double(value):\n    return value * 2\n")
    text = (ROOT / "pyproject.toml").read_text()
    text = text.replace('build-backend = "sorust.backend"\nbackend-path = ["src"]', 'build-backend = "sorust.backend"')
    text = text.replace('"setuptools>=77", "wheel>=0.45", "Cython>=3,<4"', '"sorust[build]==0.1.0", "setuptools>=77", "wheel>=0.45", "Cython>=3,<4"', 1)
    text = text.replace('name = "sorust"', 'name = "nl-atomic-example"').replace('readme = "README.md"\n', '')
    text = text.replace('sorust._compat', 'nl_atomic_example._compat').replace('artifact-package = "sorust"', 'artifact-package = "nl_atomic_example"')
    (project / "pyproject.toml").write_text(text)
    shutil.copytree(ROOT / "crates", project / "crates", ignore=shutil.ignore_patterns("target"))
    shutil.copyfile(ROOT / "MANIFEST.in", project / "MANIFEST.in")
    output = tmp_path / "external-dist"
    run([sys.executable, "-I", "-m", "build", "--no-isolation", "--outdir", output, project])
    with zipfile.ZipFile(next(output.glob("*.whl"))) as archive:
        names = archive.namelist()
        assert any(x.startswith("nl_atomic_example/_compat.") and x.endswith(".so") for x in names)
        assert any(x.startswith("nl_atomic_example/_native/") and x.endswith(".so") for x in names)
    run([python, "-I", "-m", "pip", "install", "--no-deps", next(output.glob("*.whl"))])
    run([python, "-I", "-c", '''
from nl_atomic_example import _compat
import importlib.machinery
assert any(_compat.__file__.endswith(x) for x in importlib.machinery.EXTENSION_SUFFIXES)
assert _compat.double(21) == 42
'''])


import importlib.util
import random
from sorust import NativeArtifactError, verify_artifacts
from sorust.backend import configuration

spec = importlib.util.spec_from_file_location("reference", ROOT / "src/sorust/_compat.py")
reference = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)


@pytest.mark.parametrize("data,expected", [
    (b"", 0), (b" ", 0), (b"a", 1), (b" a  b\tc\nd\r", 4),
    (b"\t\n\v\f\r", 0), (b"\x00\xff\xc2\xa0", 1),
    ("zażółć gęślą".encode(), 2), (bytes(range(256)), 3),
])
def test_reference(data, expected):
    assert reference.count_ascii_tokens(data) == expected


def test_non_bytes_rejected():
    with pytest.raises(TypeError):
        reference.count_ascii_tokens("text")


def test_source_checkout_does_not_silently_fallback():
    with pytest.raises(NativeArtifactError):
        verify_artifacts(ROOT / "src/sorust")


@pytest.mark.parametrize("change", ["../outside.toml", "/outside.toml"])
def test_manifest_escape_rejected(tmp_path, change):
    text = (ROOT / "pyproject.toml").read_text().replace(
        'rust-manifest = "crates/sorust-kernel/Cargo.toml"', f'rust-manifest = "{change}"')
    (tmp_path / "pyproject.toml").write_text(text)
    with pytest.raises(ValueError, match="inside"):
        configuration(tmp_path)


@pytest.mark.parametrize("target_location", ["inside", "outside", "missing"])
def test_lockfile_rejected_before_build(tmp_path, target_location):
    project = tmp_path / "project"
    project.mkdir()
    for name in ["pyproject.toml", "README.md", "VERSION", "MANIFEST.in"]:
        shutil.copyfile(ROOT / name, project / name)
    for name in ["src", "crates", "include"]:
        shutil.copytree(ROOT / name, project / name,
                        ignore=shutil.ignore_patterns("__pycache__", "*.egg-info", "target"))
    lockfile = project / "crates/sorust-kernel/Cargo.lock"
    content = lockfile.read_bytes()
    lockfile.unlink()
    if target_location != "missing":
        target = (project if target_location == "inside" else tmp_path) / "saved.lock"
        target.write_bytes(content)
        lockfile.symlink_to(target)
    diagnostic = "committed Cargo.lock" if target_location == "missing" else "Cargo.lock"
    with pytest.raises(ValueError, match=diagnostic):
        configuration(project)
    environment = dict(os.environ)
    environment.pop("PYTHONPATH", None)
    output = tmp_path / "dist"
    result = subprocess.run(
        [sys.executable, "-I", "-m", "build", "--sdist", "--no-isolation",
         "--outdir", str(output), str(project)],
        cwd=project, env=environment, text=True, capture_output=True, timeout=180)
    assert result.returncode != 0, result.stdout + result.stderr
    assert diagnostic in result.stdout + result.stderr
    assert not list(project.glob("build/cython/**/*.c"))
    assert not list(output.glob("*.tar.gz"))


def test_missing_artifact_rejected(tmp_path):
    (tmp_path / "sorust-artifacts.json").write_text(json.dumps({
        "schema": "sorust.artifacts/v1", "abi_version": 1,
        "artifacts": [{"kind": "python-extension", "path": "missing.so", "sha256": "0" * 64},
                      {"kind": "rust-cdylib", "path": "missing-rust.so", "sha256": "0" * 64}],
    }))
    with pytest.raises(NativeArtifactError):
        verify_artifacts(tmp_path)


def test_reference_random_bytes():
    rng = random.Random(41)
    import re
    for _ in range(200):
        value = rng.randbytes(rng.randrange(1024))
        expected = len(re.findall(rb"[^\x09-\x0d\x20]+", value))
        assert reference.count_ascii_tokens(value) == expected
