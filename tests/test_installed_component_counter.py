"""Use one pinned installed kernel directly, keeping every preparation audited."""
import gc
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import weakref

import pytest
import sorust
from sorust import backend
from test_build import ROOT, built, external_project, run
from test_nl_dsl_pilot import pilot
from test_prebuilt_component import donor, component_project
from test_rust_components import native


class Library:
    def __init__(self, *, abi=1):
        self.sorust_abi_version = lambda: abi

        def count(data, length, output):
            assert length == len(memoryview(data))
            output._obj.value = len(re.findall(rb"[^\x09-\x0d\x20]+", data))
            return 0

        self.sorust_count_ascii_tokens_v1 = count


@pytest.fixture(autouse=True)
def clear_installed_cache():
    sorust._installed_ascii_kernel.cache_clear()
    yield
    sorust._installed_ascii_kernel.cache_clear()


def test_each_preparation_audits_while_clients_share_one_binding(native, monkeypatch):
    audited, loaded = [], []
    audit = backend._rust_component

    def snapshot(config):
        result = audit(config)
        assert result["root"] == native.package.absolute()
        assert "root" not in result["provenance"]
        audited.append(config)
        return result

    def load(path):
        loaded.append(path)
        return Library()

    monkeypatch.setattr(backend, "_rust_component", snapshot)
    monkeypatch.setattr(sorust.ctypes, "CDLL", load)
    monkeypatch.setattr(sorust, "_write_export", lambda *a: pytest.fail("counter must not export"))
    before = {f.relative_to(native.package) for f in native.package.rglob("*")}
    first = sorust.prepare_ascii_token_counter(rust_component=native.spec)
    second = sorust.prepare_ascii_token_counter(rust_component=native.spec)
    assert first._library is second._library
    assert len(audited) == 2
    assert loaded == [str(native.package / "_native/libsorust_kernel.so")]
    assert "kernel_pkg" not in sys.modules
    assert first(b"one two") == second(b"one two") == 2
    class WrongLength(bytes):
        def __len__(self):
            return 99
    assert first(WrongLength(b"one two")) == 2
    assert first(b"") == 0
    with pytest.raises(TypeError):
        first("not bytes")
    assert len(audited) == 2  # Hot calls use the prepared binding.
    assert {f.relative_to(native.package) for f in native.package.rglob("*")} == before


@pytest.mark.parametrize("options", [
    {"backend": "compiled-python", "rust_component": {}},
    {"backend": "unknown", "rust_component": {}},
    {"rust_library": "other_without_component"},
])
def test_invalid_selection_does_not_resolve_or_load(monkeypatch, options):
    monkeypatch.setattr(backend.metadata, "distribution", lambda *a: pytest.fail("metadata must not resolve"))
    monkeypatch.setattr(sorust.ctypes, "CDLL", lambda *a: pytest.fail("native must not load"))
    with pytest.raises(ValueError):
        sorust.prepare_ascii_token_counter(**options)


@pytest.mark.parametrize("case", ["descriptor", "version", "pin", "library", "ownership", "drift", "linked"])
def test_bad_installed_input_fails_before_load(native, monkeypatch, case):
    spec = native.spec.copy()
    options = {}
    if case == "descriptor":
        spec = {}
    elif case == "version":
        spec["version"] = "9.9"
    elif case == "pin":
        spec["manifest-sha256"] = "0" * 64
    elif case == "library":
        options["rust_library"] = "../invalid"
    elif case == "ownership":
        native.installed.files.remove(Path("kernel_pkg/_native/libsorust_kernel.so"))
    elif case == "drift":
        (native.package / "_native/sorust.h").write_bytes(b"changed")
    else:
        path = native.package / "_native/libsorust_kernel.so"
        saved = path.with_name("saved.so")
        path.rename(saved)
        path.symlink_to(saved)
    monkeypatch.setattr(sorust.ctypes, "CDLL", lambda *a: pytest.fail("invalid component loaded"))
    with pytest.raises(sorust.NativeArtifactError):
        sorust.prepare_ascii_token_counter(rust_component=spec, **options)


def test_dual_donor_requires_explicit_default_or_build_reuse(donor, monkeypatch):
    monkeypatch.setattr(sorust.ctypes, "CDLL", lambda *a: pytest.fail("dual donor loaded"))
    with pytest.raises(sorust.NativeArtifactError, match="Rust-only"):
        sorust.prepare_ascii_token_counter(rust_component=donor.spec)


@pytest.mark.parametrize("case", ["abi", "version-symbol", "counter-symbol", "load-error"])
def test_bad_native_abi_or_symbols_never_produce_counter(native, monkeypatch, case):
    def load(path):
        if case == "load-error":
            raise OSError("loader failure")
        library = Library(abi=2 if case == "abi" else 1)
        if case in {"version-symbol", "counter-symbol"}:
            delattr(library, "sorust_abi_version" if case == "version-symbol" else "sorust_count_ascii_tokens_v1")
        return library
    monkeypatch.setattr(sorust.ctypes, "CDLL", load)
    with pytest.raises(sorust.NativeArtifactError, match="Cannot load Sorust kernel"):
        sorust.prepare_ascii_token_counter(rust_component=native.spec)
    assert sorust._installed_ascii_kernel.cache_info().currsize == 0


def test_cached_binding_does_not_bypass_new_preparation_audit(native, monkeypatch):
    loaded = []
    monkeypatch.setattr(sorust.ctypes, "CDLL", lambda path: loaded.append(path) or Library())
    counter = sorust.prepare_ascii_token_counter(rust_component=native.spec)
    (native.package / "_native/sorust.h").write_bytes(b"drift")
    assert counter(b"one two three") == 3
    with pytest.raises(sorust.NativeArtifactError):
        sorust.prepare_ascii_token_counter(rust_component=native.spec)
    assert len(loaded) == 1


def test_prepared_counter_keeps_library_after_cache_clear(native, monkeypatch):
    monkeypatch.setattr(sorust.ctypes, "CDLL", lambda path: Library())
    counter = sorust.prepare_ascii_token_counter(rust_component=native.spec)
    reference = weakref.ref(counter._library)
    sorust._installed_ascii_kernel.cache_clear()
    gc.collect()
    assert reference() is not None and counter(b"one two") == 2
    del counter
    gc.collect()
    assert reference() is None


@pytest.mark.parametrize("profile", ["source", "prebuilt"])
def test_private_root_does_not_change_old_backend_fingerprints(native, tmp_path, profile):
    path = tmp_path / "baseline_backend.py"
    path.write_bytes(subprocess.check_output(['git', '-C', str(ROOT), 'show',
        '701c89a33d41917fa5213b3decc299e605cecc5e:src/sorust/backend.py']))
    spec = importlib.util.spec_from_file_location("sorust.baseline_counter_backend", path)
    baseline = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(baseline)
    project, _, _ = external_project(tmp_path)
    if profile == "prebuilt":
        shutil.rmtree(project / "crates")
        shutil.rmtree(project / "include")
        component_project(project, native.spec)
    current = backend.configuration(project)
    previous = baseline.configuration(project)
    assert backend._source_digest(project, current) == baseline._source_digest(project, previous)


def test_real_clients_share_installed_native_handle_without_export_or_tools(built, tmp_path):
    _, _, python, sdk_root = built
    wheel, spec, _ = pilot.native_component_wheel(tmp_path, sorust.verify_artifacts(sdk_root), sdk_root)
    run([python, "-I", "-m", "pip", "install", "--no-index", "--no-deps", wheel])
    no_tools = tmp_path / "no-tools"
    no_tools.mkdir()
    env = dict(os.environ, PATH=str(no_tools))
    env.pop("PYTHONPATH", None)
    child = '''import concurrent.futures,importlib.metadata,importlib.util,json,random,re,shutil,sys
from pathlib import Path
import sorust
from sorust import backend
assert all(importlib.util.find_spec(n) is None for n in ['Cython','setuptools','wheel','build'])
assert all(shutil.which(n) is None for n in ['cargo','rustc','cc','gcc'])
spec=json.loads(sys.argv[1]);dist=importlib.metadata.distribution(spec['distribution'])
root=Path(dist.locate_file(spec['package']));before={str(p.relative_to(root)) for p in root.rglob('*')}
first=sorust.prepare_ascii_token_counter(rust_component=spec)
second=sorust.prepare_ascii_token_counter(rust_component=spec)
assert first._library is second._library and first._library._handle==second._library._handle
assert Path(first._library._name)==root/'_native/libsorust_kernel.so'
assert spec['package'] not in sys.modules
def forbidden(*a,**k):raise AssertionError('hot call attempted audit/export')
backend._rust_component=forbidden;sorust._write_export=forbidden
rng=random.Random(71);values=[b'',b'one two three',b'a\\x00b',bytes(range(256))]
values += [rng.randbytes(rng.randrange(4096)) for _ in range(200)]
expected=[len(re.findall(rb'[^\\x09-\\x0d\\x20]+',v)) for v in values]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    assert list(pool.map(first,values))==list(pool.map(second,values))==expected
sorust._installed_ascii_kernel.cache_clear();assert first(b'one two')==2
assert {str(p.relative_to(root)) for p in root.rglob('*')}==before
print('Installed donor shared handle/path, threaded parity and retained lifetime PASS')
'''
    result = subprocess.run([python, "-I", "-c", child, json.dumps(spec)], cwd=ROOT, env=env,
                            capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stdout + result.stderr
