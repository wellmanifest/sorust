"""Sorust runtime. Building consumers requires sorust[build] in build-system."""
from __future__ import annotations

import ctypes
import hashlib
import importlib
import importlib.machinery
import importlib.util
import json
import re
import sys
from collections.abc import Callable, Generator, Iterable
from functools import lru_cache
from itertools import islice
from operator import index
from pathlib import Path, PurePosixPath
from typing import SupportsIndex

__version__ = "0.1.0"
__all__ = ["count_ascii_tokens", "count_ascii_tokens_many", "iter_ascii_token_counts",
           "prepare_ascii_token_counter", "verify_artifacts", "export_artifacts", "NativeArtifactError"]


class NativeArtifactError(RuntimeError):
    """A required native file or resource is missing or fails validation."""


def _resource_path(value: str) -> Path:
    """One explicit data file, relative to the artifact package."""
    if (not isinstance(value, str) or not value or any(c in value for c in "\\:*?[]")
            or any(ord(character) < 32 for character in value)):
        raise ValueError("resource path must be a canonical package-relative POSIX path")
    relative = PurePosixPath(value)
    if (not relative.parts or relative.is_absolute() or ".." in relative.parts
            or relative.as_posix() != value
            or relative.parts[0].casefold() in {"_native", "sorust-artifacts.json"}
            or relative.suffix.lower() in {".py", ".pyc", ".pyo", ".pyw", ".so", ".pyd", ".dll", ".dylib"}):
        raise ValueError("unsafe or reserved resource path")
    return Path(*relative.parts)


def _resource_entries(manifest: dict) -> list:
    if manifest["schema"] in {"sorust.artifacts/v1", "sorust.rust-component/v1"}:
        if "resources" in manifest:
            raise ValueError("declared resources require manifest v2")
        return []
    resources = manifest["resources"]
    if not isinstance(resources, list):
        raise ValueError("manifest v2 requires a resources list")
    occupied = {Path(item["path"]) for item in manifest["artifacts"] + manifest.get("headers", [])}
    for item in resources:
        if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
            raise ValueError("resource entries require path and sha256")
        relative = _resource_path(item["path"])
        if relative in occupied:
            raise ValueError("conflicting resource path")
        occupied.add(relative)
    return resources


def _rust_component_manifest(manifest: dict) -> None:
    fields = {"schema", "abi_version", "package", "platform", "rustc", "source_sha256", "headers", "artifacts"}
    if (set(manifest) != fields or type(manifest["abi_version"]) is not int
            or not isinstance(manifest["package"], str)
            or not re.fullmatch(r"[a-zA-Z_]\w*(?:\.[a-zA-Z_]\w*)*", manifest["package"])
            or any(not isinstance(manifest[key], str) or not manifest[key].strip() for key in ["platform", "rustc"])
            or not isinstance(manifest["source_sha256"], str)
            or not re.fullmatch(r"[0-9a-f]{64}", manifest["source_sha256"])):
        raise ValueError("Rust component requires exact identity, ABI and source/compiler fields")
    artifacts, headers = manifest["artifacts"], manifest["headers"]
    if (not isinstance(artifacts, list) or len(artifacts) != 1 or not isinstance(headers, list)
            or not isinstance(artifacts[0], dict) or artifacts[0].get("kind") != "rust-cdylib"):
        raise ValueError("Rust component requires exactly one Rust library and a headers list")
    entries = [(artifacts[0], {"kind", "path", "sha256"}, {".so", ".dylib", ".dll"})]
    entries += [(item, {"path", "sha256"}, {".h"}) for item in headers]
    occupied = set()
    for item, keys, suffixes in entries:
        if (not isinstance(item, dict) or set(item) != keys or not isinstance(item["path"], str)
                or any(c in item["path"] for c in "\\:") or any(ord(c) < 32 for c in item["path"])
                or not isinstance(item["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", item["sha256"])):
            raise ValueError("invalid Rust component payload entry")
        relative = PurePosixPath(item["path"])
        if (len(relative.parts) != 2 or relative.parts[0] != "_native"
                or relative.as_posix() != item["path"] or relative.suffix not in suffixes
                or relative in occupied):
            raise ValueError("Rust component requires unique canonical direct _native library/header paths")
        occupied.add(relative)


def verify_artifacts(package_dir: str | Path | None = None) -> dict:
    """Verify packaged bytes; hashes detect drift, not publisher authenticity."""
    root = Path(package_dir) if package_dir is not None else Path(__file__).parent
    try:
        manifest = json.loads((root / "sorust-artifacts.json").read_text())
        native = manifest["schema"] == "sorust.rust-component/v1"
        if manifest["schema"] not in {"sorust.artifacts/v1", "sorust.artifacts/v2", "sorust.rust-component/v1"} or manifest["abi_version"] != 1:
            raise ValueError("unsupported manifest or ABI")
        artifacts = manifest["artifacts"]
        if native:
            if package_dir is None:
                raise ValueError("default Sorust SDK requires a dual-artifact manifest")
            _rust_component_manifest(manifest)
            metadata = (root / "sorust-artifacts.json").absolute()
            if not metadata.is_file() or any(p.is_symlink() for p in [metadata, *metadata.parents]):
                raise ValueError("Rust component metadata must be a regular unlinked file")
        else:
            kinds = [item["kind"] for item in artifacts]
            if (kinds.count("rust-cdylib") != 1 or "python-extension" not in kinds
                    or set(kinds) != {"rust-cdylib", "python-extension"}):
                raise ValueError("both native artifact kinds are required")
        resources = _resource_entries(manifest)
        resource_paths = {Path(item["path"]) for item in resources}
        for item in artifacts + manifest.get("headers", []) + resources:
            relative = Path(item["path"])
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError("unsafe artifact path")
            path = root / relative
            if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
                raise ValueError("artifact escapes package")
            if native and (not path.is_file() or any(p.is_symlink() for p in path.absolute().parents)):
                raise ValueError("Rust component payload must be a regular unlinked file")
            if relative in resource_paths and any(p.is_symlink() for p in path.parents):
                raise ValueError("resource path contains a symlink")
            if hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
                raise ValueError("artifact checksum mismatch")
        return manifest
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise NativeArtifactError(f"Invalid Sorust artifacts: {error}") from error


def export_artifacts(destination: str | Path, *, package_dir: str | Path | None = None) -> Path:
    """Copy verified native files and declared resources; write the manifest last.

    The destination's parent must exist. Existing destinations are never reused.
    A failed copy can leave an incomplete output; no compiler or loader runs.
    """
    root = Path(package_dir) if package_dir is not None else Path(__file__).parent
    manifest = verify_artifacts(package_dir)
    payload = {}
    for item in manifest["artifacts"] + manifest.get("headers", []) + manifest.get("resources", []):
        relative = Path(item["path"])
        if relative in payload or relative == Path("sorust-artifacts.json"):
            raise NativeArtifactError(f"Conflicting export path: {relative}")
        try:
            data = (root / relative).read_bytes()
        except OSError as error:
            raise NativeArtifactError(f"Cannot snapshot artifact: {relative}") from error
        if hashlib.sha256(data).hexdigest() != item["sha256"]:
            raise NativeArtifactError(f"Artifact changed before export: {relative}")
        payload[relative] = data
    manifest_bytes = (json.dumps(manifest, indent=2) + "\n").encode()
    target = Path(destination)
    target.mkdir()
    for relative, data in payload.items():
        path = target / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as output:
            output.write(data)
    with (target / "sorust-artifacts.json").open("xb") as output:
        output.write(manifest_bytes)
    return target.resolve()


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


def _compiled():
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
    return module


def count_ascii_tokens(data: bytes, *, backend: str = "rust") -> int:
    """Count whitespace-delimited byte tokens using the selected native backend."""
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    if type(data) is not bytes:
        data = memoryview(data).tobytes()
    if backend == "compiled-python":
        return _compiled().count_ascii_tokens(data)
    if backend != "rust":
        raise ValueError("backend must be rust or compiled-python")
    _, function = _kernel()
    output = ctypes.c_uint64()
    status = function(data, len(data), ctypes.byref(output))
    if status:
        raise NativeArtifactError(f"Rust kernel returned status {status}")
    return output.value


class _PreparedAsciiTokenCounter:
    __slots__ = ("_function", "_library")

    def __init__(self, function, library=None):
        self._function = function
        self._library = library

    def __call__(self, data: bytes) -> int:
        if not isinstance(data, bytes):
            raise TypeError("data must be bytes")
        if type(data) is not bytes:
            data = memoryview(data).tobytes()
        if self._library is None:
            return self._function(data)
        output = ctypes.c_uint64()
        status = self._function(data, len(data), ctypes.byref(output))
        if status:
            raise NativeArtifactError(f"Rust kernel returned status {status}")
        return output.value


def prepare_ascii_token_counter(*, backend: str = "rust") -> Callable[[bytes], int]:
    """Audit artifacts and bind a native scalar counter for repeated calls.

    The callable retains its native entry and Rust library. Calls do not audit
    files again; use verify_artifacts or prepare anew to detect on-disk drift.
    Process loader caches remain in effect; this is not a hot-reload API.
    """
    if backend == "compiled-python":
        try:
            function = _compiled().count_ascii_tokens
        except AttributeError as error:
            raise NativeArtifactError("Compiled Python scalar entry required") from error
        if not callable(function):
            raise NativeArtifactError("Compiled Python scalar entry required")
        return _PreparedAsciiTokenCounter(function)
    if backend != "rust":
        raise ValueError("backend must be rust or compiled-python")
    verify_artifacts()
    library, function = _kernel()
    return _PreparedAsciiTokenCounter(function, library)


@lru_cache(maxsize=1)
def _many_kernel():
    library, _ = _kernel()
    try:
        function = library.sorust_count_ascii_tokens_many_v1
        function.argtypes = [ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t),
                             ctypes.c_size_t, ctypes.POINTER(ctypes.c_uint64)]
        function.restype = ctypes.c_int32
        return library, function
    except AttributeError as error:
        raise NativeArtifactError("Cannot load Sorust batch kernel") from error


def count_ascii_tokens_many(inputs: Iterable[bytes], *, backend: str = "rust") -> list[int]:
    """Count each byte buffer in order; Rust batches join buffers for one FFI call."""
    values = []
    for data in inputs:
        if not isinstance(data, bytes):
            raise TypeError("inputs must contain bytes")
        if type(data) is not bytes:
            data = memoryview(data).tobytes()
        values.append(data)
    if backend == "compiled-python":
        try:
            function = _compiled().count_ascii_tokens_many
        except AttributeError as error:
            raise NativeArtifactError("Compiled Python batch entry required") from error
        return function(values)
    if backend != "rust":
        raise ValueError("backend must be rust or compiled-python")
    joined = b"".join(values)
    lengths = (ctypes.c_size_t * len(values))(*(len(data) for data in values))
    output = (ctypes.c_uint64 * len(values))()
    _, function = _many_kernel()
    status = function(joined, len(joined), lengths, len(values), output)
    if status:
        raise NativeArtifactError(f"Rust batch kernel returned status {status}")
    return list(output)


def iter_ascii_token_counts(inputs: Iterable[bytes], *, batch_size: SupportsIndex = 256,
                           backend: str = "rust") -> Generator[int, None, None]:
    """Lazily yield counts, consuming at most one batch ahead of the caller.

    Validate parameters eagerly. Native capability is checked on first pull,
    before touching the source. The caller retains ownership of that source.
    """
    if isinstance(batch_size, bool):
        raise TypeError("batch_size must be an integer")
    try:
        size = index(batch_size)
    except TypeError:
        raise TypeError("batch_size must be an integer") from None
    if not 1 <= size <= sys.maxsize:
        raise ValueError("batch_size must be between 1 and sys.maxsize")
    if backend not in ("rust", "compiled-python"):
        raise ValueError("backend must be rust or compiled-python")

    def generate():
        count_ascii_tokens_many([], backend=backend)
        source = iter(inputs)
        while True:
            batch = list(islice(source, size))
            if not batch:
                return
            yield from count_ascii_tokens_many(batch, backend=backend)

    return generate()
