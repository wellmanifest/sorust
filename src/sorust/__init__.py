"""Sorust runtime. Building consumers requires sorust[build] in build-system."""
from __future__ import annotations

import ctypes
import hashlib
import importlib
import importlib.machinery
import importlib.util
import json
from functools import lru_cache
from pathlib import Path

__version__ = "0.1.0"
__all__ = ["count_ascii_tokens", "verify_artifacts", "NativeArtifactError"]


class NativeArtifactError(RuntimeError):
    """A required binary is missing, incompatible or fails integrity checks."""


def verify_artifacts(package_dir: str | Path | None = None) -> dict:
    """Verify packaged bytes; hashes detect drift, not publisher authenticity."""
    root = Path(package_dir) if package_dir is not None else Path(__file__).parent
    try:
        manifest = json.loads((root / "sorust-artifacts.json").read_text())
        if manifest["schema"] != "sorust.artifacts/v1" or manifest["abi_version"] != 1:
            raise ValueError("unsupported manifest or ABI")
        artifacts = manifest["artifacts"]
        kinds = [item["kind"] for item in artifacts]
        if (kinds.count("rust-cdylib") != 1 or "python-extension" not in kinds
                or set(kinds) != {"rust-cdylib", "python-extension"}):
            raise ValueError("both native artifact kinds are required")
        for item in artifacts + manifest.get("headers", []):
            relative = Path(item["path"])
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError("unsafe artifact path")
            path = root / relative
            if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
                raise ValueError("artifact escapes package")
            if hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
                raise ValueError("artifact checksum mismatch")
        return manifest
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise NativeArtifactError(f"Invalid Sorust artifacts: {error}") from error


@lru_cache(maxsize=1)
def _kernel():
    manifest = verify_artifacts()
    item = next(x for x in manifest["artifacts"] if x["kind"] == "rust-cdylib")
    try:
        library = ctypes.CDLL(str(Path(__file__).parent / item["path"]))
        library.sorust_abi_version.argtypes = []
        library.sorust_abi_version.restype = ctypes.c_uint32
        if library.sorust_abi_version() != 1:
            raise ValueError("loaded Rust ABI differs from v1")
        function = library.sorust_count_ascii_tokens_v1
        function.argtypes = [ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_uint64)]
        function.restype = ctypes.c_int32
        return library, function
    except (OSError, AttributeError, ValueError) as error:
        raise NativeArtifactError(f"Cannot load Sorust kernel: {error}") from error


def count_ascii_tokens(data: bytes, *, backend: str = "rust") -> int:
    """Count whitespace-delimited byte tokens using the selected native backend."""
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    if type(data) is not bytes:
        data = memoryview(data).tobytes()
    if backend == "compiled-python":
        manifest = verify_artifacts()
        name = __name__ + "._compat"
        try:
            spec = importlib.util.find_spec(name)
        except (ImportError, ValueError) as error:
            raise NativeArtifactError("Cannot resolve compiled Python extension") from error
        if (spec is None or not spec.origin
                or not isinstance(spec.loader, importlib.machinery.ExtensionFileLoader)):
            raise NativeArtifactError("compiled Python extension required")
        verified = {(Path(__file__).parent / item["path"]).resolve()
                    for item in manifest["artifacts"] if item["kind"] == "python-extension"}
        selected = Path(spec.origin).resolve()
        if selected not in verified:
            raise NativeArtifactError("compiled Python extension is not listed in artifact manifest")
        module = importlib.import_module(name)
        if Path(module.__file__).resolve() != selected:
            raise NativeArtifactError("imported Python extension differs from verified origin")
        return module.count_ascii_tokens(data)
    if backend != "rust":
        raise ValueError("backend must be rust or compiled-python")
    _, function = _kernel()
    output = ctypes.c_uint64()
    status = function(data, len(data), ctypes.byref(output))
    if status:
        raise NativeArtifactError(f"Rust kernel returned status {status}")
    return output.value
