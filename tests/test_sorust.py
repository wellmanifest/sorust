import importlib.util
import json
import random
from pathlib import Path

import pytest

from sorust import NativeArtifactError, verify_artifacts
from sorust.backend import configuration

ROOT = Path(__file__).resolve().parents[1]
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
