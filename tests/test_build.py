"""Real build/install/link tests; all compiler and runtime processes are exercised."""
import json
import hashlib
import ctypes
import os
from pathlib import Path
import shutil
import subprocess
import sys
import sysconfig
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


@pytest.mark.parametrize("entrypoint", ["api", "cli"])
def test_installed_export_has_standalone_native_consumers(built, tmp_path, entrypoint):
    _, _, python, package = built
    destination = tmp_path / "bundle"
    if entrypoint == "api":
        output = run([python, "-I", "-c", '''
import sys, sorust
print(sorust.export_artifacts(sys.argv[1], package_dir=sys.argv[2]))
''', destination, package])
    else:
        output = run([python, "-I", "-m", "sorust", "export", destination])
    assert Path(output.strip()) == destination
    manifest = json.loads((package / "sorust-artifacts.json").read_text())
    assert json.loads((destination / "sorust-artifacts.json").read_text()) == manifest
    expected = {"sorust-artifacts.json"}
    for item in manifest["artifacts"] + manifest["headers"]:
        expected.add(item["path"])
        data = (destination / item["path"]).read_bytes()
        assert data == (package / item["path"]).read_bytes()
        assert hashlib.sha256(data).hexdigest() == item["sha256"]
    assert {path.relative_to(destination).as_posix() for path in destination.rglob("*")
            if path.is_file()} == expected
    extension = destination / next(item["path"] for item in manifest["artifacts"]
                                   if item["kind"] == "python-extension")
    runtime = tmp_path / "standalone"
    venv.EnvBuilder(with_pip=False).create(runtime)
    run([runtime / "bin/python", "-I", "-c", '''
import importlib.util, sys
assert importlib.util.find_spec("sorust") is None
assert importlib.util.find_spec("Cython") is None
spec = importlib.util.spec_from_file_location("_compat", sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
assert module.count_ascii_tokens(b"one two") == 2
assert module.count_ascii_tokens_many([b"one two", b""]) == [2, 0]
''', extension])
    library = destination / next(item["path"] for item in manifest["artifacts"]
                                 if item["kind"] == "rust-cdylib")
    source = tmp_path / "export-client.c"
    source.write_text('''#include "sorust.h"
int main(void) { uint64_t n=0; const uint8_t text[]="one two\\tthree";
return !(sorust_abi_version()==1 && sorust_count_ascii_tokens_v1(text, sizeof(text)-1, &n)==0 && n==3); }
''')
    binary = tmp_path / "export-client"
    run(["cc", source, "-I", destination / "_native", library,
         "-Wl,-rpath," + str(library.parent), "-o", binary])
    run([binary])


@pytest.mark.parametrize("entrypoint", ["api", "cli"])
@pytest.mark.parametrize("kind", ["empty", "populated", "file", "symlink"])
def test_export_preserves_existing_destination(built, tmp_path, entrypoint, kind):
    _, _, python, _ = built
    destination = tmp_path / "occupied"
    if kind == "file":
        destination.write_bytes(b"keep")
    elif kind == "symlink":
        actual = tmp_path / "actual"
        actual.mkdir()
        (actual / "keep").write_bytes(b"keep")
        destination.symlink_to(actual, target_is_directory=True)
    else:
        destination.mkdir()
        if kind == "populated":
            (destination / "keep").write_bytes(b"keep")
    if entrypoint == "api":
        run([python, "-I", "-c", '''
import sorust, sys
try: sorust.export_artifacts(sys.argv[1])
except FileExistsError: pass
else: raise AssertionError("existing destination reused")
''', destination])
    else:
        result = subprocess.run([python, "-I", "-m", "sorust", "export", destination],
                                text=True, capture_output=True, timeout=30)
        assert result.returncode == 1 and "sorust:" in result.stderr
        assert not result.stdout and "Traceback" not in result.stderr
    if kind == "file":
        assert destination.read_bytes() == b"keep"
    else:
        assert sorted(path.name for path in destination.iterdir()) == ([] if kind == "empty" else ["keep"])
        if kind != "empty":
            assert (destination / "keep").read_bytes() == b"keep"
        if kind == "symlink":
            assert destination.is_symlink() and destination.readlink() == actual


@pytest.mark.parametrize("case", ["missing", "corrupt", "escape", "duplicate"])
def test_export_rejects_invalid_source_before_output(built, tmp_path, case):
    _, _, python, package = built
    clone = tmp_path / "source"
    shutil.copytree(package, clone)
    manifest_path = clone / "sorust-artifacts.json"
    manifest = json.loads(manifest_path.read_text())
    item = manifest["artifacts"][0]
    if case == "missing":
        (clone / item["path"]).unlink()
    elif case == "corrupt":
        (clone / item["path"]).write_bytes(b"corrupt")
    elif case == "escape":
        item["path"] = "../outside.so"
    else:
        manifest["headers"].append(dict(item))
    manifest_path.write_text(json.dumps(manifest))
    destination = tmp_path / "bundle"
    run([python, "-I", "-c", '''
import sys, sorust
try: sorust.export_artifacts(sys.argv[1], package_dir=sys.argv[2])
except sorust.NativeArtifactError: pass
else: raise AssertionError("invalid export source accepted")
''', destination, clone])
    assert not destination.exists()


def test_export_rechecks_snapshot_before_output(built, tmp_path, monkeypatch):
    import sorust
    clone = tmp_path / "source"
    shutil.copytree(built[3], clone)
    original = sorust.verify_artifacts

    def change_after_verification(root):
        manifest = original(root)
        path = clone / manifest["artifacts"][0]["path"]
        path.write_bytes(path.read_bytes() + b"changed")
        return manifest

    monkeypatch.setattr(sorust, "verify_artifacts", change_after_verification)
    destination = tmp_path / "bundle"
    with pytest.raises(sorust.NativeArtifactError, match="changed before export"):
        sorust.export_artifacts(destination, package_dir=clone)
    assert not destination.exists()


def test_export_interrupted_copy_has_no_completion_manifest(built, tmp_path, monkeypatch):
    import sorust
    manifest = sorust.verify_artifacts(built[3])
    destination = tmp_path / "bundle"
    library = destination / next(item["path"] for item in manifest["artifacts"]
                                 if item["kind"] == "rust-cdylib")
    original = Path.open

    def fail_copy(path, mode="r", *args, **kwargs):
        if path == library and mode == "xb":
            raise OSError("controlled write failure")
        return original(path, mode, *args, **kwargs)

    monkeypatch.setattr(Path, "open", fail_copy)
    with pytest.raises(OSError, match="controlled write failure"):
        sorust.export_artifacts(destination, package_dir=built[3])
    assert destination.is_dir()
    assert not (destination / "sorust-artifacts.json").exists()


def test_sdist_has_native_sources(built):
    output, _, _, _ = built
    with tarfile.open(next(output.glob("*.tar.gz"))) as archive:
        names = archive.getnames()
        assert not any("/build/" in name or "/target/" in name for name in names)
        for suffix in ("crates/sorust-kernel/Cargo.lock", "crates/sorust-kernel/src/lib.rs",
                       "include/sorust.h", "src/sorust/backend.py"):
            assert any(name.endswith(suffix) for name in names)


@pytest.mark.parametrize("api", ["scalar", "many"])
@pytest.mark.parametrize("case", ["unlisted", "source", "missing", "preloaded"])
def test_compiled_import_requires_manifest_bound_native_module(built, tmp_path, case, api):
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
    if sys.argv[4] == "scalar":
        sorust.count_ascii_tokens(b"one two", backend="compiled-python")
    else:
        sorust.count_ascii_tokens_many([b"one two"], backend="compiled-python")
except sorust.NativeArtifactError:
    pass
else:
    raise AssertionError("unlisted compiled module accepted")
assert not Path(sys.argv[3]).exists(), "uncompiled Python executed before rejection"
if sys.argv[2] != "preloaded":
    assert "sorust._compat" not in sys.modules, "unverified module imported before rejection"
''', tmp_path, case, marker, api])


def test_c_consumer_links_installed_binary(built, tmp_path):
    _, _, _, package = built
    manifest = json.loads((package / "sorust-artifacts.json").read_text())
    library = package / next(x["path"] for x in manifest["artifacts"] if x["kind"] == "rust-cdylib")
    source = tmp_path / "consumer.c"
    source.write_text('''#include "sorust.h"
int main(void) { uint64_t n=0; const uint8_t text[]="one two\\tthree";
uint64_t counts[3]; size_t lengths[]={3,0,sizeof(text)-1-3};
if (sorust_count_ascii_tokens_many_v1(text,sizeof(text)-1,lengths,3,counts)!=0 ||
    counts[0]!=1 || counts[1]!=0 || counts[2]!=2) return 2;
lengths[2]++; counts[0]=counts[1]=counts[2]=77;
if (sorust_count_ascii_tokens_many_v1(text,sizeof(text)-1,lengths,3,counts)!=1 ||
    counts[0]!=77 || counts[1]!=77 || counts[2]!=77) return 3;
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
    run([python, "-I", "-c", r'''
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
    assert sorust.count_ascii_tokens_many([payload, b"a\x00b", b""], backend=backend) == [2, 1, 0]
assert reference.count_ascii_tokens_many([payload, b"a\x00b", b""]) == [2, 1, 0]
''', ROOT / "src/sorust/_compat.py", case])


@pytest.mark.parametrize("backend", ["rust", "compiled-python"])
def test_installed_many_parity(built, backend):
    run([built[2], "-I", "-c", r'''
import importlib.util, random, sys, sorust
spec=importlib.util.spec_from_file_location("reference", sys.argv[1])
reference=importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)
rng=random.Random(4242)
values=[b"", b"a", b"b", b"\x00\xff", bytes(range(256)), "zażółć gęślą".encode()]
values += [rng.randbytes(rng.randrange(2048)) for _ in range(300)]
expected=reference.count_ascii_tokens_many(values)
assert sorust.count_ascii_tokens_many(values,backend=sys.argv[2]) == expected
assert sorust.count_ascii_tokens_many(iter(values),backend=sys.argv[2]) == expected
assert sorust.count_ascii_tokens_many([],backend=sys.argv[2]) == []
assert sorust.count_ascii_tokens_many([b"a",b"b"],backend=sys.argv[2]) == [1,1]
''', ROOT / "src/sorust/_compat.py", backend])


def test_many_normalizes_buffers_before_ffi(monkeypatch):
    import sorust

    class Misleading(bytes):
        def __len__(self): return 1024
        def __bytes__(self): return b"wrong"
        def __iter__(self): return iter([32])

    calls = []

    def capture(data, length, lengths, count, output):
        assert data == b"one twoa\x00b" and length == 10
        assert list(lengths) == [7, 3, 0] and count == 3
        output[0], output[1], output[2] = 2, 1, 0
        calls.append(count)
        return 0

    monkeypatch.setattr(sorust, "_many_kernel", lambda: (None, capture))
    assert sorust.count_ascii_tokens_many([Misleading(b"one two"), b"a\x00b", b""]) == [2, 1, 0]
    assert calls == [3]


def test_many_native_error_is_explicit(monkeypatch):
    import sorust

    def reject(data, length, lengths, count, output):
        output[0] = 99
        return 1

    monkeypatch.setattr(sorust, "_many_kernel", lambda: (None, reject))
    with pytest.raises(sorust.NativeArtifactError, match="status 1"):
        sorust.count_ascii_tokens_many([b"one"])


@pytest.mark.parametrize("inputs", [b"one", [b"a", "text"], [bytearray(b"a")], [memoryview(b"a")], None, 42])
def test_many_invalid_inputs_fail_before_ffi(monkeypatch, inputs):
    import sorust

    def forbidden():
        raise AssertionError("invalid inputs reached native loader")

    monkeypatch.setattr(sorust, "_many_kernel", forbidden)
    with pytest.raises(TypeError):
        sorust.count_ascii_tokens_many(inputs)


def test_many_invalid_backend():
    import sorust
    with pytest.raises(ValueError, match="backend"):
        sorust.count_ascii_tokens_many([b"one"], backend="unknown")


@pytest.mark.parametrize("backend", ["rust", "compiled-python"])
def test_source_many_empty_batch_requires_native_artifacts(backend):
    import sorust
    with pytest.raises(sorust.NativeArtifactError):
        sorust.count_ascii_tokens_many([], backend=backend)


def test_many_legacy_scalar_library_remains_usable(built, tmp_path):
    clone = tmp_path / "sorust"
    shutil.copytree(built[3], clone)
    manifest_path = clone / "sorust-artifacts.json"
    manifest = json.loads(manifest_path.read_text())
    entry = next(item for item in manifest["artifacts"] if item["kind"] == "rust-cdylib")
    source = tmp_path / "legacy.c"
    source.write_text('''#include <stddef.h>
#include <stdint.h>
uint32_t sorust_abi_version(void) { return 1; }
int32_t sorust_count_ascii_tokens_v1(const uint8_t *data,size_t length,uint64_t *output) {
if (!data || length!=7 || !output) return 1; *output=2; return 0; }
''')
    library = clone / entry["path"]
    run(["cc", "-shared", "-fPIC", source, "-o", library])
    entry["sha256"] = hashlib.sha256(library.read_bytes()).hexdigest()
    manifest_path.write_text(json.dumps(manifest))
    run([built[2], "-I", "-c", '''
import sys
sys.path.insert(0,sys.argv[1])
import sorust
assert sorust.count_ascii_tokens(b"one two") == 2
try: sorust.count_ascii_tokens_many([b"one two"])
except sorust.NativeArtifactError as error: assert "batch" in str(error)
else: raise AssertionError("missing batch symbol silently accepted")
''', tmp_path])


def test_many_missing_compiled_entry_is_explicit(built):
    run([built[2], "-I", "-c", '''
import sorust
assert sorust.count_ascii_tokens(b"one two",backend="compiled-python") == 2
from sorust import _compat
del _compat.count_ascii_tokens_many
try: sorust.count_ascii_tokens_many([b"one two"],backend="compiled-python")
except sorust.NativeArtifactError as error: assert "batch" in str(error)
else: raise AssertionError("missing compiled batch entry silently accepted")
'''])


@pytest.mark.parametrize("backend", ["rust", "compiled-python"])
def test_stream_is_lazy_and_bounds_prefetch(monkeypatch, backend):
    import sorust
    consumed, calls = [], []

    def inputs():
        for value in range(7):
            consumed.append(value)
            yield str(value).encode()

    def many(values, *, backend):
        calls.append((backend, tuple(values)))
        return [int(value) for value in values]

    monkeypatch.setattr(sorust, "count_ascii_tokens_many", many)
    results = sorust.iter_ascii_token_counts(inputs(), batch_size=3, backend=backend)
    assert consumed == calls == []
    assert next(results) == 0 and consumed == [0, 1, 2]
    assert next(results) == 1 and next(results) == 2 and consumed == [0, 1, 2]
    assert next(results) == 3 and consumed == [0, 1, 2, 3, 4, 5]
    assert list(results) == [4, 5, 6] and consumed == list(range(7))
    assert [len(values) for _, values in calls] == [0, 3, 3, 1]
    assert all(selected == backend for selected, _ in calls)


@pytest.mark.parametrize("size", [0, -1, sys.maxsize + 1])
def test_stream_invalid_size_is_eager(size):
    import sorust

    class Untouched:
        def __iter__(self):
            raise AssertionError("source touched")

    with pytest.raises(ValueError, match="batch_size"):
        sorust.iter_ascii_token_counts(Untouched(), batch_size=size)


@pytest.mark.parametrize("size", [True, False, 1.5, "2", None])
def test_stream_invalid_size_type_is_eager(size):
    import sorust

    class Untouched:
        def __iter__(self):
            raise AssertionError("source touched")

    with pytest.raises(TypeError, match="batch_size"):
        sorust.iter_ascii_token_counts(Untouched(), batch_size=size)


def test_stream_invalid_backend_is_eager():
    import sorust

    class Untouched:
        def __iter__(self):
            raise AssertionError("source touched")

    with pytest.raises(ValueError, match="backend"):
        sorust.iter_ascii_token_counts(Untouched(), backend="unknown")


def test_stream_accepts_integer_index_size(monkeypatch):
    import sorust

    class Size:
        def __index__(self): return 2

    calls = []

    def many(values, *, backend):
        calls.append(len(values))
        return [len(value) for value in values]

    monkeypatch.setattr(sorust, "count_ascii_tokens_many", many)
    assert list(sorust.iter_ascii_token_counts([b"a", b"bb", b""], batch_size=Size())) == [1, 2, 0]
    assert calls == [0, 2, 1]


def test_stream_close_preserves_caller_source(monkeypatch):
    import sorust
    consumed, closed = [], []

    def inputs():
        try:
            for value in range(7):
                consumed.append(value)
                yield str(value).encode()
        finally:
            closed.append(True)

    monkeypatch.setattr(sorust, "count_ascii_tokens_many", lambda values, **kwargs: [int(value) for value in values])
    source = inputs()
    results = sorust.iter_ascii_token_counts(source, batch_size=3)
    assert next(results) == 0 and consumed == [0, 1, 2]
    results.close()
    assert consumed == [0, 1, 2] and closed == []
    assert next(source) == b"3"
    source.close()
    assert closed == [True]


def test_stream_source_error_discards_incomplete_batch(monkeypatch):
    import sorust
    marker = RuntimeError("controlled source error")
    calls = []

    def inputs():
        yield b"0"
        yield b"1"
        yield b"2"
        raise marker

    def many(values, **kwargs):
        calls.append(tuple(values))
        return [int(value) for value in values]

    monkeypatch.setattr(sorust, "count_ascii_tokens_many", many)
    results = sorust.iter_ascii_token_counts(inputs(), batch_size=2)
    assert next(results) == 0 and next(results) == 1
    with pytest.raises(RuntimeError) as error:
        next(results)
    assert error.value is marker and calls == [(), (b"0", b"1")]


def test_stream_native_error_precedes_source_consumption(monkeypatch):
    import sorust

    class Untouched:
        def __iter__(self):
            raise AssertionError("source touched")

    def reject(values, **kwargs):
        assert values == []
        raise sorust.NativeArtifactError("controlled missing capability")

    monkeypatch.setattr(sorust, "count_ascii_tokens_many", reject)
    results = sorust.iter_ascii_token_counts(Untouched())
    with pytest.raises(sorust.NativeArtifactError, match="capability"):
        next(results)


@pytest.mark.parametrize("backend", ["rust", "compiled-python"])
def test_source_stream_empty_requires_native_artifacts(backend):
    import sorust
    with pytest.raises(sorust.NativeArtifactError):
        list(sorust.iter_ascii_token_counts([], backend=backend))


@pytest.mark.parametrize("backend", ["rust", "compiled-python"])
def test_installed_stream_parity_and_errors(built, backend):
    run([built[2], "-I", "-c", r'''
import itertools, random, sys, sorust
rng=random.Random(9876)
class Misleading(bytes):
    def __len__(self): return 1024
    def __bytes__(self): return b"wrong"
    def __iter__(self): return iter([32])
values=[b"",b"a\x00b",bytes(range(256)),"zażółć gęślą".encode(),Misleading(b"one two")]
values += [rng.randbytes(rng.randrange(1024)) for _ in range(300)]
expected=sorust.count_ascii_tokens_many(values,backend=sys.argv[1])
for size in [1,7,256,1000]:
    assert list(sorust.iter_ascii_token_counts(iter(values),batch_size=size,backend=sys.argv[1])) == expected
assert list(sorust.iter_ascii_token_counts([],backend=sys.argv[1])) == []
infinite=sorust.iter_ascii_token_counts(itertools.repeat(b"one two"),batch_size=3,backend=sys.argv[1])
assert list(itertools.islice(infinite,5)) == [2]*5
infinite.close()
source=iter([b"one",b"two","invalid",b"four",b"five"])
results=sorust.iter_ascii_token_counts(source,batch_size=2,backend=sys.argv[1])
assert next(results)==1 and next(results)==1
try: next(results)
except TypeError: pass
else: raise AssertionError("invalid batch accepted")
assert next(source)==b"five"
''', backend])


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


def external_project(tmp_path, layout="single"):
    project = tmp_path / "external"
    package = project / "src/nl_atomic_example"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("")
    (package / "_compat.py").write_text("def double(value):\n    return value * 2\n")
    (package / "untouched.py").write_text("def identity(value):\n    return value\n")
    modules = ["nl_atomic_example._compat"]
    if layout == "nested":
        (package / "nested").mkdir()
        (package / "nested/__init__.py").write_text("")
        (package / "nested/_fast.py").write_text("def triple(value):\n    return value * 3\n")
        modules.append("nl_atomic_example.nested._fast")
    text = (ROOT / "pyproject.toml").read_text()
    text = text.replace('build-backend = "sorust.backend"\nbackend-path = ["src"]', 'build-backend = "sorust.backend"')
    text = text.replace('"setuptools>=77", "wheel>=0.45", "Cython>=3,<4"', '"sorust[build]==0.1.0", "setuptools>=77", "wheel>=0.45", "Cython>=3,<4"', 1)
    text = text.replace('name = "sorust"', 'name = "nl-atomic-example"').replace('readme = "README.md"\n', '')
    text = text.replace('sorust._compat', 'nl_atomic_example._compat').replace('artifact-package = "sorust"', 'artifact-package = "nl_atomic_example"')
    text = text.replace('python-modules = ["nl_atomic_example._compat"]',
                        "python-modules = " + json.dumps(modules))
    (project / "pyproject.toml").write_text(text)
    shutil.copytree(ROOT / "crates", project / "crates", ignore=shutil.ignore_patterns("target"))
    shutil.copytree(ROOT / "include", project / "include")
    shutil.copyfile(ROOT / "MANIFEST.in", project / "MANIFEST.in")
    return project, package, modules


@pytest.mark.parametrize("layout", ["single", "nested"])
def test_external_consumer_build_backend(built, tmp_path, layout):
    _, wheel, python, _ = built
    run([sys.executable, "-I", "-m", "pip", "install", "--no-deps", "--force-reinstall", wheel])
    project, package, modules = external_project(tmp_path, layout)
    output = tmp_path / "external-dist"
    run([sys.executable, "-I", "-m", "build", "--no-isolation", "--outdir", output, project])
    with zipfile.ZipFile(next(output.glob("*.whl"))) as archive:
        names = archive.namelist()
        assert any(x.startswith("nl_atomic_example/_compat.") and x.endswith(".so") for x in names)
        assert any(x.startswith("nl_atomic_example/_native/") and x.endswith(".so") for x in names)
        assert "nl_atomic_example/untouched.py" in names
        for name in modules:
            assert name.replace(".", "/") + ".py" not in names
        manifest = json.loads(archive.read("nl_atomic_example/sorust-artifacts.json"))
        assert manifest["package"] == "nl_atomic_example"
        assert sum(item["kind"] == "python-extension" for item in manifest["artifacts"]) == len(modules)
        assert sum(item["kind"] == "rust-cdylib" for item in manifest["artifacts"]) == 1
        assert [item["path"] for item in manifest["headers"]] == ["_native/sorust.h"]
        for item in manifest["artifacts"] + manifest["headers"]:
            assert hashlib.sha256(archive.read("nl_atomic_example/" + item["path"])).hexdigest() == item["sha256"]
    run([python, "-I", "-m", "pip", "install", "--no-deps", "--force-reinstall", next(output.glob("*.whl"))])
    run([python, "-I", "-c", '''
from nl_atomic_example import _compat, untouched
import ctypes, importlib.machinery, json, sys
from pathlib import Path
assert any(_compat.__file__.endswith(x) for x in importlib.machinery.EXTENSION_SUFFIXES)
assert _compat.double(21) == 42
assert untouched.identity("value") == "value"
if sys.argv[1] == "nested":
    from nl_atomic_example.nested import _fast
    assert any(_fast.__file__.endswith(x) for x in importlib.machinery.EXTENSION_SUFFIXES)
    assert _fast.triple(14) == 42
package = Path(_compat.__file__).parent
manifest = json.loads((package / "sorust-artifacts.json").read_text())
item = next(item for item in manifest["artifacts"] if item["kind"] == "rust-cdylib")
library = ctypes.CDLL(str(package / item["path"]))
library.sorust_abi_version.argtypes = []
library.sorust_abi_version.restype = ctypes.c_uint32
assert library.sorust_abi_version() == 1
count = library.sorust_count_ascii_tokens_v1
count.argtypes = [ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_uint64)]
count.restype = ctypes.c_int32
output = ctypes.c_uint64()
assert count(b"one two", 7, ctypes.byref(output)) == 0 and output.value == 2
from sorust import export_artifacts, verify_artifacts
exported = export_artifacts(sys.argv[2], package_dir=package)
assert verify_artifacts(exported) == manifest
assert not list(exported.rglob("*.py"))
''', layout, tmp_path / "foreign-export"])


@pytest.mark.parametrize("former_source", ["changed", "removed"])
def test_consumer_wheel_rebuild_drops_stale_outputs(built, tmp_path, former_source):
    _, wheel, python, _ = built
    run([sys.executable, "-I", "-m", "pip", "install", "--no-deps", "--force-reinstall", wheel])
    project, package, _ = external_project(tmp_path)
    first = tmp_path / "first"
    run([sys.executable, "-I", "-m", "build", "--wheel", "--no-isolation", "--outdir", first, project])
    # Model an interrupted older packager leaving its installation payload behind.
    old_staging = project / "build" / ("bdist." + sysconfig.get_platform()) / "wheel"
    with zipfile.ZipFile(next(first.glob("*.whl"))) as archive:
        for name in archive.namelist():
            if name.startswith("nl_atomic_example/"):
                target = old_staging / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.read(name))
    config = project / "pyproject.toml"
    config.write_text(config.read_text().replace("nl_atomic_example._compat", "nl_atomic_example.untouched"))
    if former_source == "changed":
        (package / "_compat.py").write_text("def double(value):\n    return value * 3\n")
    else:
        (package / "_compat.py").unlink()
    second = tmp_path / "second"
    run([sys.executable, "-I", "-m", "build", "--wheel", "--no-isolation", "--outdir", second, project])
    rebuilt = next(second.glob("*.whl"))
    with zipfile.ZipFile(rebuilt) as archive:
        names = archive.namelist()
        assert not any(name.startswith("nl_atomic_example/_compat.") and name.endswith(".so") for name in names)
        assert ("nl_atomic_example/_compat.py" in names) == (former_source == "changed")
        assert "nl_atomic_example/untouched.py" not in names
        manifest = json.loads(archive.read("nl_atomic_example/sorust-artifacts.json"))
        extensions = [item["path"] for item in manifest["artifacts"] if item["kind"] == "python-extension"]
        assert len(extensions) == 1 and extensions[0].startswith("untouched.")
        for item in manifest["artifacts"] + manifest["headers"]:
            assert hashlib.sha256(archive.read("nl_atomic_example/" + item["path"])).hexdigest() == item["sha256"]
    # Install only the second wheel: stale imports must not depend on a prior install.
    run([python, "-I", "-m", "pip", "install", "--no-deps", "--force-reinstall", rebuilt])
    run([python, "-I", "-c", '''
import importlib, importlib.machinery, sys
from nl_atomic_example import untouched
assert isinstance(untouched.__loader__, importlib.machinery.ExtensionFileLoader)
assert untouched.identity(42) == 42
if sys.argv[1] == "changed":
    from nl_atomic_example import _compat
    assert isinstance(_compat.__loader__, importlib.machinery.SourceFileLoader)
    assert _compat.double(9) == 27
else:
    try:
        importlib.import_module("nl_atomic_example._compat")
    except ModuleNotFoundError:
        pass
    else:
        raise AssertionError("removed module survived rebuild")
''', former_source])


def test_consumer_wheel_rebuild_rejects_skip_build(built, tmp_path):
    _, wheel, _, _ = built
    run([sys.executable, "-I", "-m", "pip", "install", "--no-deps", "--force-reinstall", wheel])
    project, _, _ = external_project(tmp_path)
    output = tmp_path / "skipped"
    result = subprocess.run([sys.executable, "-I", "-c", '''
import sys
from sorust.backend import build_wheel
build_wheel(sys.argv[1], {"--build-option": ["--skip-build"]})
''', str(output)], cwd=project, text=True, capture_output=True, timeout=180)
    assert result.returncode != 0
    assert "--skip-build is unsupported" in result.stderr
    assert not list(output.glob("*.whl"))


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
