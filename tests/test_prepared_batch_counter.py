"""Prepared batch calls reuse audited native entries and existing buffer rules."""
import gc
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from types import SimpleNamespace
import weakref

import pytest
import sorust
from sorust import backend
from test_build import ROOT, built, run
from test_installed_component_counter import Library, clear_installed_cache
from test_nl_dsl_pilot import pilot
from test_prebuilt_component import donor
from test_rust_components import native


class BatchLibrary(Library):
    def __init__(self, calls, *, status=0):
        super().__init__()

        def batch(data, total, lengths, count, output):
            assert total == len(data) == sum(lengths) and count == len(lengths)
            offset = 0
            for i, length in enumerate(lengths):
                output[i] = len(re.findall(rb"[^\x09-\x0d\x20]+", data[offset:offset + length]))
                offset += length
            calls.append((data, list(lengths), count))
            return status

        self.sorust_count_ascii_tokens_many_v1 = batch


def test_prepared_batch_shares_scalar_handle_and_makes_one_ffi_per_batch(native, monkeypatch):
    loaded, calls, audits = [], [], []
    snapshot = backend._rust_component
    def audit(config):
        audits.append(config)
        return snapshot(config)
    monkeypatch.setattr(backend, "_rust_component", audit)
    monkeypatch.setattr(sorust.ctypes, "CDLL", lambda path: loaded.append(path) or BatchLibrary(calls))
    scalar = sorust.prepare_ascii_token_counter(rust_component=native.spec)
    counter = sorust.prepare_ascii_token_batch_counter(rust_component=native.spec)
    assert scalar._library is counter._library
    assert len(loaded) == 1 and len(audits) == 2 and "kernel_pkg" not in sys.modules
    class Misleading(bytes):
        def __len__(self): return 99
        def __iter__(self): return iter([32])
        def __bytes__(self): return b"wrong"
    def forbidden(*a, **k):
        pytest.fail("hot call audited or exported")
    monkeypatch.setattr(backend, "_rust_component", forbidden)
    monkeypatch.setattr(sorust, "verify_artifacts", forbidden)
    monkeypatch.setattr(sorust, "_write_export", forbidden)
    assert counter(iter([Misleading(b"one two"), b"a\x00b", b""])) == [2, 1, 0]
    assert calls == [(b"one twoa\x00b", [7, 3, 0], 3)]
    assert counter([]) == []
    assert calls[-1] == (b"", [], 0) and len(calls) == 2


@pytest.mark.parametrize("inputs", [None, 42, b"one", ["text"], [bytearray(b"a")], [memoryview(b"a")]])
def test_invalid_hot_inputs_never_reach_ffi(native, monkeypatch, inputs):
    calls = []
    monkeypatch.setattr(sorust.ctypes, "CDLL", lambda path: BatchLibrary(calls))
    counter = sorust.prepare_ascii_token_batch_counter(rust_component=native.spec)
    with pytest.raises(TypeError):
        counter(inputs)
    assert calls == []


def test_status_error_does_not_return_partially_written_results(native, monkeypatch):
    calls = []
    monkeypatch.setattr(sorust.ctypes, "CDLL", lambda path: BatchLibrary(calls, status=7))
    counter = sorust.prepare_ascii_token_batch_counter(rust_component=native.spec)
    with pytest.raises(sorust.NativeArtifactError, match="status 7"):
        counter([b"one two"])
    assert len(calls) == 1


@pytest.mark.parametrize("options", [
    {"backend": "unknown"},
    {"backend": "compiled-python", "rust_component": {}},
    {"rust_library": "custom_without_component"},
])
def test_invalid_selection_fails_before_resolution(monkeypatch, options):
    monkeypatch.setattr(backend.metadata, "distribution", lambda *a: pytest.fail("metadata resolved"))
    monkeypatch.setattr(sorust.ctypes, "CDLL", lambda *a: pytest.fail("native loaded"))
    with pytest.raises(ValueError):
        sorust.prepare_ascii_token_batch_counter(**options)


def test_missing_batch_symbol_preserves_scalar_counter(native, monkeypatch):
    monkeypatch.setattr(sorust.ctypes, "CDLL", lambda path: Library())
    scalar = sorust.prepare_ascii_token_counter(rust_component=native.spec)
    with pytest.raises(sorust.NativeArtifactError, match="batch kernel"):
        sorust.prepare_ascii_token_batch_counter(rust_component=native.spec)
    assert scalar(b"one two") == 2


def test_cached_handle_never_bypasses_audit_for_new_batch_preparation(native, monkeypatch):
    loaded, calls = [], []
    monkeypatch.setattr(sorust.ctypes, "CDLL", lambda path: loaded.append(path) or BatchLibrary(calls))
    counter = sorust.prepare_ascii_token_batch_counter(rust_component=native.spec)
    (native.package / "_native/sorust.h").write_bytes(b"drift")
    assert counter([b"one two"]) == [2]
    with pytest.raises(sorust.NativeArtifactError):
        sorust.prepare_ascii_token_batch_counter(rust_component=native.spec)
    assert len(loaded) == 1


def test_batch_preparation_rejects_wrong_pin_before_loading(native, monkeypatch):
    monkeypatch.setattr(sorust.ctypes, "CDLL", lambda *a: pytest.fail("wrong pin loaded"))
    with pytest.raises(sorust.NativeArtifactError, match="pin mismatch"):
        sorust.prepare_ascii_token_batch_counter(rust_component=native.spec | {"manifest-sha256": "0" * 64})


def test_prepared_batch_retains_library_after_cache_clear(native, monkeypatch):
    monkeypatch.setattr(sorust.ctypes, "CDLL", lambda path: BatchLibrary([]))
    counter = sorust.prepare_ascii_token_batch_counter(rust_component=native.spec)
    reference = weakref.ref(counter._library)
    sorust._installed_ascii_kernel.cache_clear()
    gc.collect()
    assert reference() is not None and counter([b"one two", b""]) == [2, 0]
    del counter
    gc.collect()
    assert reference() is None


@pytest.mark.parametrize("entry", [None, 42])
def test_compiled_batch_entry_must_be_callable(monkeypatch, entry):
    module = SimpleNamespace() if entry is None else SimpleNamespace(count_ascii_tokens_many=entry)
    monkeypatch.setattr(sorust, "_compiled", lambda: module)
    with pytest.raises(sorust.NativeArtifactError, match="Compiled Python batch entry"):
        sorust.prepare_ascii_token_batch_counter(backend="compiled-python")


def test_compiled_prepared_batch_audits_only_during_preparation(monkeypatch):
    audits, calls = [], []
    def count(values):
        calls.append(values)
        assert all(type(value) is bytes for value in values)
        return [len(re.findall(rb"[^\x09-\x0d\x20]+", value)) for value in values]
    monkeypatch.setattr(sorust, "_compiled", lambda: audits.append(1) or SimpleNamespace(count_ascii_tokens_many=count))
    counter = sorust.prepare_ascii_token_batch_counter(backend="compiled-python")
    class Bytes(bytes): pass
    assert counter(iter([Bytes(b"one two"), b""])) == [2, 0]
    assert counter([]) == []
    assert audits == [1] and len(calls) == 2


def test_real_sdk_and_installed_batch_clients_parity_lifetime_and_threads(built, tmp_path):
    _, _, python, sdk_root = built
    wheel, spec, _ = pilot.native_component_wheel(tmp_path, sorust.verify_artifacts(sdk_root), sdk_root)
    run([python, "-I", "-m", "pip", "install", "--no-index", "--no-deps", wheel])
    tools = tmp_path / "no-tools"
    tools.mkdir()
    env = dict(os.environ, PATH=str(tools))
    env.pop("PYTHONPATH", None)
    code = '''import concurrent.futures,importlib.metadata,importlib.util,json,random,re,shutil,sys
from pathlib import Path
import sorust
from sorust import backend
assert all(importlib.util.find_spec(n) is None for n in ['Cython','setuptools','wheel','build'])
assert all(shutil.which(n) is None for n in ['cargo','rustc','cc','gcc'])
spec=json.loads(sys.argv[1]);root=Path(importlib.metadata.distribution(spec['distribution']).locate_file(spec['package']))
before={str(p.relative_to(root)) for p in root.rglob('*')}
scalar=sorust.prepare_ascii_token_counter(rust_component=spec)
a=sorust.prepare_ascii_token_batch_counter(rust_component=spec)
b=sorust.prepare_ascii_token_batch_counter(rust_component=spec)
default=sorust.prepare_ascii_token_batch_counter()
compiled=sorust.prepare_ascii_token_batch_counter(backend='compiled-python')
assert a._library is b._library is scalar._library
assert Path(a._library._name)==root/'_native/libsorust_kernel.so'
assert spec['package'] not in sys.modules
def forbidden(*a,**k):raise AssertionError('hot batch audited or exported')
backend._rust_component=forbidden;sorust.verify_artifacts=forbidden;sorust._write_export=forbidden
rng=random.Random(83);values=[b'',b'a',b'b',b'one two',b'a\\x00b',bytes(range(256))]
values += [rng.randbytes(rng.randrange(2048)) for _ in range(80)]
expected=[len(re.findall(rb'[^\\x09-\\x0d\\x20]+',v)) for v in values]
for counter in [a,b,default,compiled]:
    assert counter(iter(values))==expected and counter([])==[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    assert list(pool.map(a,[values]*12))==list(pool.map(b,[values]*12))==[expected]*12
sorust._installed_ascii_kernel.cache_clear();assert a([b'one two'])==[2]
assert {str(p.relative_to(root)) for p in root.rglob('*')}==before
print('Prepared native/default/compiled batch parity, shared scalar handle and retained lifetime PASS')
'''
    result = subprocess.run([python, "-I", "-c", code, json.dumps(spec)], cwd=ROOT, env=env,
                            capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stdout + result.stderr
