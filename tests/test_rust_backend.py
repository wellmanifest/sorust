"""Native source production and reuse share the dual backend's build contract."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tarfile
import zipfile

import pytest
import sorust
from sorust import backend, rust_backend
from test_build import ROOT, built, external_project, run
from test_prebuilt_component import donor, component_project


def source_project(parent):
    root = parent / "producer"
    root.mkdir()
    token = hashlib.sha256(str(root).encode()).hexdigest()[:10]
    name, package = "sorust-source-fixture-" + token, "source_kernel_" + token
    for file in ["crates/sorust-kernel/Cargo.toml", "crates/sorust-kernel/Cargo.lock",
                 "crates/sorust-kernel/src/lib.rs", "include/sorust.h"]:
        target = root / file
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / file, target)
    (root / "pyproject.toml").write_text(f'''[build-system]
requires = ["sorust==0.1.0", "setuptools>=77", "wheel>=0.45"]
build-backend = "sorust.rust_backend"
[project]
name = "{name}"
version = "0.0.0"
requires-python = ">=3.11"
[tool.sorust]
rust-manifest = "crates/sorust-kernel/Cargo.toml"
rust-library = "sorust_kernel"
artifact-package = "{package}"
abi-version = 1
''')
    return root, name, package


@pytest.fixture
def producer(tmp_path):
    return source_project(tmp_path)


def test_native_configuration_and_build_requirements_do_not_require_python(producer):
    root, _, _ = producer
    config = rust_backend.configuration(root)
    assert "python-modules" not in config and "resources" not in config
    assert rust_backend.get_requires_for_build_wheel() == ["setuptools>=77", "wheel>=0.45"]
    assert rust_backend.get_requires_for_build_sdist() == rust_backend.get_requires_for_build_wheel()
    assert not (root / "src").exists()


@pytest.mark.parametrize("case", ["python-modules", "resources", "prebuilt", "abi-bool", "setuptools",
    "dependencies", "optional-dependencies", "scripts", "gui-scripts", "entry-points", "dynamic",
    "missing-version", "python-source", "lib-path", "source-link", "header-link", "lock-link"])
def test_native_configuration_rejects_mixed_or_unsafe_sources(producer, case):
    root, _, _ = producer
    path = root / "pyproject.toml"
    text = path.read_text()
    if case in {"python-modules", "resources"}:
        text += case + ' = []\n'
    elif case == "prebuilt":
        text = text.replace('rust-manifest = "crates/sorust-kernel/Cargo.toml"', 'rust-component = {}')
    elif case == "abi-bool":
        text = text.replace('abi-version = 1', 'abi-version = true')
    elif case == "setuptools":
        text += '\n[tool.setuptools]\npackages = []\n'
    elif case in {"dependencies", "optional-dependencies", "scripts", "gui-scripts", "entry-points", "dynamic"}:
        value = {'dependencies': '["other"]', 'optional-dependencies': '{feature=["other"]}',
                 'scripts': '{}', 'gui-scripts': '{}', 'entry-points': '{}', 'dynamic': '["description"]'}[case]
        text = text.replace('[project]\n', '[project]\n' + case + ' = ' + value + '\n')
    elif case == "missing-version":
        text = text.replace('version = "0.0.0"\n', '')
    elif case == "python-source":
        (root / "src").mkdir()
        (root / "src/unwanted.py").write_text('raise AssertionError("must not execute")\n')
    elif case == "lib-path":
        cargo = root / "crates/sorust-kernel/Cargo.toml"
        cargo.write_text(cargo.read_text().replace('[lib]', '[lib]\npath="other.rs"'))
    else:
        relative = {'source-link': 'crates/sorust-kernel/src/lib.rs', 'header-link': 'include/sorust.h',
                    'lock-link': 'crates/sorust-kernel/Cargo.lock'}[case]
        source = root / relative
        saved = source.with_name('saved-' + source.name)
        source.rename(saved)
        source.symlink_to(saved)
    path.write_text(text)
    with pytest.raises(ValueError):
        rust_backend.configuration(root)


def test_shared_input_fingerprint_preserves_legacy_dual_and_prebuilt_order(donor, tmp_path):
    path = tmp_path / "legacy_backend.py"
    path.write_bytes(subprocess.check_output(['git', '-C', str(ROOT), 'show',
        '5e96b66883e99b390816464b5e44f5c04443caec:src/sorust/backend.py']))
    spec = importlib.util.spec_from_file_location("sorust.legacy_backend", path)
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    project, _, _ = external_project(tmp_path)
    config = backend.configuration(project)
    assert backend._source_digest(project, config) == old._source_digest(project, config)
    shutil.rmtree(project / "crates")
    shutil.rmtree(project / "include")
    component_project(project, donor.spec)
    config = backend.configuration(project)
    assert backend._source_digest(project, config) == old._source_digest(project, config)


def test_native_sdist_wheel_without_cython_and_downstream_reuse(built, producer, tmp_path):
    _, sdk, runtime, _ = built
    run([sys.executable, "-I", "-m", "pip", "install", "--no-index", "--no-deps", "--force-reinstall", sdk])
    root, distribution, package = producer
    cargo = root / "crates/sorust-kernel/Cargo.toml"
    cargo.write_text(cargo.read_text().replace('[package]', '[package]\nbuild="../shared-build.rs"'))
    (root / "crates/shared-build.rs").write_text('fn main() {}\n')
    output = tmp_path / "native-dist"
    output.mkdir()
    run([sys.executable, "-I", "-c", '''
import sys,os,tarfile,importlib.abc
from pathlib import Path
class NoCython(importlib.abc.MetaPathFinder):
    def find_spec(self,name,path=None,target=None):
        if name=="Cython" or name.startswith("Cython."):
            raise ModuleNotFoundError("Cython blocked by source producer regression")
sys.meta_path.insert(0,NoCython())
from sorust import rust_backend
root,out=map(Path,sys.argv[1:]);os.chdir(root)
sdist=rust_backend.build_sdist(str(out))
unpacked=out/'unpacked';unpacked.mkdir()
with tarfile.open(out/sdist) as archive:archive.extractall(unpacked,filter="data")
project,=unpacked.iterdir();os.chdir(project)
rust_backend.build_wheel(str(out))
assert not any(name=="Cython" or name.startswith("Cython.") for name in sys.modules)
''', root, output])
    with tarfile.open(next(output.glob('*.tar.gz'))) as archive:
        names = {'/'.join(Path(name).parts[1:]) for name in archive.getnames()}
        assert {'pyproject.toml', 'crates/sorust-kernel/Cargo.toml', 'crates/sorust-kernel/Cargo.lock',
                'crates/sorust-kernel/src/lib.rs', 'crates/shared-build.rs', 'include/sorust.h'} <= names
        assert not any(name.endswith(('.so', '.dll', '.dylib')) for name in names)
    wheel = next(output.glob('*.whl'))
    assert 'py3-none-linux_x86_64' in wheel.name
    with zipfile.ZipFile(wheel) as archive:
        assert not any(name.endswith(('.py', '.pyc', '.pyd')) for name in archive.namelist())
        raw = archive.read(package + '/sorust-artifacts.json')
        manifest = json.loads(raw)
        assert manifest['schema'] == 'sorust.rust-component/v1'
        assert manifest['source_sha256'] == backend._source_digest(root, rust_backend.configuration(root))
    spec = {'distribution': distribution, 'version': '0.0.0', 'package': package,
            'manifest-sha256': hashlib.sha256(raw).hexdigest()}
    assert run([sys.executable, '-I', '-c', 'import importlib.metadata,sys;\ntry: importlib.metadata.distribution(sys.argv[1])\nexcept importlib.metadata.PackageNotFoundError: print("absent")', distribution]).strip() == 'absent'
    run([sys.executable, '-I', '-m', 'pip', 'install', '--no-index', '--no-deps', wheel])
    try:
        exported = tmp_path / 'source-export'
        run([sys.executable, '-I', '-c', '''
import sys,importlib.metadata,json,ctypes
from pathlib import Path
from sorust import verify_artifacts,export_artifacts
dist,package,target=sys.argv[1:]
root=Path(importlib.metadata.distribution(dist).locate_file(package))
assert package not in sys.modules
manifest=verify_artifacts(root);export_artifacts(target,package_dir=root)
assert verify_artifacts(target)==manifest
lib=ctypes.CDLL(str(Path(target)/'_native/libsorust_kernel.so'))
lib.sorust_abi_version.restype=ctypes.c_uint32;assert lib.sorust_abi_version()==1
fn=lib.sorust_count_ascii_tokens_v1;fn.argtypes=[ctypes.c_char_p,ctypes.c_size_t,ctypes.POINTER(ctypes.c_uint64)];fn.restype=ctypes.c_int32
value=ctypes.c_uint64();assert fn(b'one two three',13,ctypes.byref(value))==0 and value.value==3
''', distribution, package, exported])
        consumer_parent = tmp_path / 'consumer-case'
        consumer_parent.mkdir()
        consumer, _, _ = external_project(consumer_parent)
        shutil.rmtree(consumer / 'crates')
        shutil.rmtree(consumer / 'include')
        component_project(consumer, spec)
        tools = tmp_path / 'no-rust'
        tools.mkdir()
        marker = tmp_path / 'rust-called'
        for name in ['cargo', 'rustc']:
            tool = tools / name
            tool.write_text('#!/bin/sh\nprintf "%s\\n" ' + name + ' >> ' + shlex.quote(str(marker)) + '\nexit 97\n')
            tool.chmod(0o755)
        env = dict(os.environ, PATH=str(tools) + os.pathsep + os.environ.get('PATH', ''))
        env.pop('PYTHONPATH', None)
        out = tmp_path / 'consumer-dist'
        result = subprocess.run([sys.executable, '-I', '-m', 'build', '--no-isolation', '--outdir', str(out), str(consumer)],
                                cwd=ROOT, env=env, text=True, capture_output=True, timeout=180)
        assert result.returncode == 0, result.stdout + result.stderr
        assert not marker.exists()
        result_wheel = next(out.glob('*.whl'))
        with zipfile.ZipFile(result_wheel) as archive:
            cm = json.loads(archive.read('nl_atomic_example/sorust-artifacts.json'))
            assert cm['rust_component']['manifest_sha256'] == spec['manifest-sha256']
            assert cm['headers'] == manifest['headers']
            assert next(x for x in cm['artifacts'] if x['kind']=='rust-cdylib') == manifest['artifacts'][0]
        run([runtime, '-I', '-m', 'pip', 'install', '--no-index', '--no-deps', '--force-reinstall', result_wheel])
        run([runtime, '-I', '-c', '''
import ctypes
from pathlib import Path
from nl_atomic_example import _compat
assert _compat.double(7)==14
lib=ctypes.CDLL(str(Path(_compat.__file__).parent/'_native/libsorust_kernel.so'))
lib.sorust_abi_version.restype=ctypes.c_uint32
assert lib.sorust_abi_version()==1
'''])
    finally:
        run([sys.executable, '-I', '-m', 'pip', 'uninstall', '--yes', distribution])
