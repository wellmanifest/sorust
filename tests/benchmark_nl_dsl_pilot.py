"""Offline, pinned NL DSL consumer pilot; run with the approved Wellman executor.

Build dependencies and a current Sorust wheel/rlib must already exist locally.
Consumer files are read from Git objects, never from a mutable working tree.
"""
from __future__ import annotations

import argparse
import cProfile
import ctypes
from dataclasses import asdict
import hashlib
import importlib
import importlib.machinery
import importlib.util
import inspect
import json
import os
from pathlib import Path
import platform
import pstats
import re
import shutil
import statistics
import subprocess
import sys
import time
import timeit
import tomllib
import venv
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REVISION = "aa47c8752f1ea446208f6dfb7a018ad02e92250a"
FILES = ("standard/__init__.py", "standard/nl_dsl_llm.py",
         "standard/semantic-profile.json", "standard/test_conformance.py", "LICENSE")
QUERIES = ["pokaż otwarte zadania", "wypisz otwarte tickety", "wyświetl zadania",
           "show open tickets", "list open tasks", "display tickets", "ticket.list",
           "ticket.list status=OPEN", "nie sprawdzaj stanu klastra produkcyjnego",
           "stan klastra produkcyjnego", "unknown query", "", " \t\n",
           "ticket.create title='zażółć'", "ticket.list\u00a0status=OPEN"]
COMMANDS = ["ticket.list", "ticket.list status=OPEN", "ticket.list filter:status=CLOSED",
            "ticket.create title='zażółć'", "list ticket status=OPEN"]
READ_QUERIES = ["ticket.list", "pokaż otwarte zadania", "show open tickets",
                "ticket.list status=CLOSED"]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def snapshot(repository, revision, files=FILES):
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("revision must be an exact lowercase 40-hex commit")
    prefix = ["git", "-C", str(repository)]
    if subprocess.check_output([*prefix, "cat-file", "-t", revision]).strip() != b"commit":
        raise ValueError("revision must identify a commit")
    return {name: subprocess.check_output([*prefix, "show", revision + ":" + name]) for name in files}


def new_output(root, requested):
    path = requested if requested.is_absolute() else root / requested
    if ".." in path.parts or not path.is_relative_to(root / ".subactor/cache"):
        raise ValueError("output must be a new directory inside this checkout's .subactor/cache")
    if any(p.is_symlink() for p in [path, *path.parents]):
        raise ValueError("output path must not contain symlinks")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.mkdir()  # Never reuse or erase a previous run.
    return path


def check_wheel(wheel, root):
    with zipfile.ZipFile(wheel) as archive:
        for name in ["__init__.py", "backend.py"]:
            if archive.read("sorust/" + name) != (root / "src/sorust" / name).read_bytes():
                raise ValueError("Sorust wheel must match this checkout's runtime and backend")


def execute(args, cwd, log, *, environment=None, timeout=600):
    started = time.perf_counter()
    env = dict(os.environ) if environment is None else dict(environment)
    env.pop("PYTHONPATH", None)
    result = subprocess.run([str(x) for x in args], cwd=cwd, env=env, text=True,
                            capture_output=True, timeout=timeout)
    log.write_text(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}); see {log}")
    return time.perf_counter() - started


def samples(function, number):
    function()
    values = [x / number for x in timeit.repeat(function, number=number, repeat=7)]
    return {"number": number, "median_seconds": statistics.median(values), "samples_seconds": values}


def compare(observations):
    reference = observations["source"]["observations"]
    for mode in ["wheel", "exported"]:
        if observations[mode]["observations"] != reference:
            raise ValueError(f"consumer behavior differs in {mode} mode")
    return digest(json.dumps(reference, ensure_ascii=False, sort_keys=True).encode())


def conformance(path):
    spec = importlib.util.spec_from_file_location("pilot_conformance", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    tests = [(name, item) for name, item in vars(module).items()
             if name.startswith("test_") and inspect.isfunction(item)]
    if not tests or any(inspect.signature(item).parameters for _, item in tests):
        raise ValueError("pilot requires nonempty, argument-free pinned conformance tests")
    for _, test in tests:
        test()  # Fail the run on any assertion; do not silently skip tests.
    return [name for name, _ in tests]


def worker(run, mode, report):
    config = json.loads((run / "run.json").read_text())
    assert importlib.util.find_spec("sorust") is None
    assert importlib.util.find_spec("Cython") is None
    assert all(shutil.which(name) is None for name in ["cargo", "rustc", "cc", "gcc"])
    if mode == "source":
        sys.path.insert(0, str(run / "reference/src"))
    elif mode == "exported":
        sys.path.insert(0, str(run / "exported"))
    module = importlib.import_module("standard.nl_dsl_llm")
    expected_loader = (importlib.machinery.SourceFileLoader if mode == "source"
                       else importlib.machinery.ExtensionFileLoader)
    assert isinstance(module.__loader__, expected_loader)
    assert digest(Path(module.__file__).read_bytes()) == config["moduleHashes"][mode]
    assert digest(Path(module.__file__).with_name("semantic-profile.json").read_bytes()) == config["profileSha256"]
    passed = conformance(run / "conformance.py")
    library_path = run / "shared-kernel" / config["rustArtifact"]["path"]
    assert digest(library_path.read_bytes()) == config["rustArtifact"]["sha256"]
    library = ctypes.CDLL(str(library_path))
    library.sorust_abi_version.argtypes = []
    library.sorust_abi_version.restype = ctypes.c_uint32
    assert library.sorust_abi_version() == 1
    many = library.sorust_count_ascii_tokens_many_v1
    many.argtypes = [ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t),
                     ctypes.c_size_t, ctypes.POINTER(ctypes.c_uint64)]
    many.restype = ctypes.c_int32

    def native(texts):
        encoded = [text.encode("utf-8") for text in texts]
        joined = b"".join(encoded)
        lengths = (ctypes.c_size_t * len(encoded))(*map(len, encoded))
        output = (ctypes.c_uint64 * len(encoded))()
        if many(joined, len(joined), lengths, len(encoded), output) != 0:
            raise RuntimeError("Rust batch call failed")
        return list(output)

    compatible = [q for q in QUERIES if all(not c.isspace() or c in " \t\n\r\v\f" for c in q)]
    assert native(compatible) == [len(q.split()) for q in compatible]
    parser = module.NLIntentParser()
    spec = importlib.util.spec_from_file_location("pilot_fixture", run / "conformance.py")
    fixture = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fixture)
    bridge, _ = fixture.create_test_fixture()
    results = [bridge.handle_request(q) for q in READ_QUERIES]
    whitespace = []
    for separator in ["\u00a0", "\u2003", "\x1c", "\u3000"]:
        text = "ticket.list" + separator + "status=OPEN"
        whitespace.append({"separator": f"U+{ord(separator):04X}", "unicodeCount": len(text.split()),
                           "rustAsciiCount": native([text])[0],
                           "consumerArguments": module.DSLCommand.from_text(text).arguments})
    assert all(x["unicodeCount"] != x["rustAsciiCount"] for x in whitespace)
    observations = {
        "parse": [asdict(value) if value is not None else None for value in map(parser.parse, QUERIES)],
        "canonical": [module.DSLCommand.from_text(q).to_canonical_string() for q in COMMANDS],
        "bridge": [{"success": x.success, "status": x.status, "data": x.data,
                    "errors": x.errors, "sourceLayer": x.meta.get("sourceLayer")} for x in results],
        "whitespace": whitespace, "rustCompatibleCounts": native(compatible),
    }
    workloads = {"parse": lambda: [parser.parse(q) for q in QUERIES],
                 "dsl_roundtrip": lambda: [module.DSLCommand.from_text(q).to_canonical_string() for q in COMMANDS],
                 "bridge": lambda: [bridge.handle_request(q) for q in READ_QUERIES],
                 "rust_batch_with_encoding": lambda: native(compatible),
                 "python_unicode_split_compatible_inputs": lambda: [len(q.split()) for q in compatible]}
    measurements = {name: samples(fn, config["number"]) for name, fn in workloads.items()}
    profile = cProfile.Profile()
    profile.runcall(lambda: [workloads["parse"]() for _ in range(config["number"])])
    stats = pstats.Stats(profile)
    top = [{"file": Path(key[0]).name, "line": key[1], "function": key[2],
            "calls": value[1], "cumulativeSeconds": value[3]}
           for key, value in sorted(stats.stats.items(), key=lambda x: x[1][3], reverse=True)[:8]]
    write_json(report, {"mode": mode, "python": sys.version, "platform": platform.platform(),
                        "loader": type(module.__loader__).__name__, "conformanceTests": passed,
                        "observations": observations, "measurements": measurements,
                        "parseProfile": top, "sharedRustSha256": digest(library_path.read_bytes()),
                        "runtimeWithoutSorustCythonOrToolchain": True})


def pilot(args):
    import sorust

    inputs = snapshot(args.consumer_root, args.revision)
    check_wheel(args.sorust_wheel, ROOT)
    if not args.rust_rlib.is_file() or args.rust_rlib.is_symlink():
        raise ValueError("rust-rlib must be a regular prebuilt library")
    import sorust.backend
    assert Path(sorust.backend.__file__).read_bytes() == (ROOT / "src/sorust/backend.py").read_bytes()
    manifest = sorust.verify_artifacts()
    rustc = subprocess.check_output(["rustc", "-vV"], text=True).strip()
    if rustc != manifest["rustc"]:
        raise ValueError("rlib consumer requires the Sorust artifact's exact Rust toolchain")
    run = new_output(ROOT, args.output)
    for name, data in inputs.items():
        target = run / "reference/src" / name if name.startswith("standard/") else run / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    (run / "conformance.py").write_bytes(inputs["standard/test_conformance.py"])
    project = run / "consumer"
    package = project / "src/standard"
    package.mkdir(parents=True)
    for name in ["__init__.py", "nl_dsl_llm.py", "semantic-profile.json"]:
        (package / name).write_bytes(inputs["standard/" + name])
    (project / "LICENSE").write_bytes(inputs["LICENSE"])
    own_revision = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    own_files = ["crates/sorust-kernel/Cargo.toml", "crates/sorust-kernel/Cargo.lock",
                 "crates/sorust-kernel/src/lib.rs", "include/sorust.h"]
    for name, data in snapshot(ROOT, own_revision, own_files).items():
        target = project / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    version = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]["version"]
    (project / "pyproject.toml").write_text(f'''[build-system]
requires = ["sorust[build]=={version}", "setuptools>=77", "wheel>=0.45", "Cython>=3,<4"]
build-backend = "sorust.backend"
[project]
name = "sorust-nl-dsl-pilot"
version = "0.0.0"
requires-python = ">=3.11"
dependencies = []
[tool.setuptools.packages.find]
where = ["src"]
[tool.setuptools.package-data]
standard = ["semantic-profile.json"]
[tool.sorust]
python-modules = ["standard.__init__", "standard.nl_dsl_llm"]
rust-manifest = "crates/sorust-kernel/Cargo.toml"
rust-library = "sorust_kernel"
artifact-package = "standard"
abi-version = 1
''')
    (project / "MANIFEST.in").write_text("recursive-include crates *.toml *.lock *.rs\nrecursive-include include *.h\nrecursive-include src *.py *.json\n")
    build_seconds = execute([sys.executable, "-I", "-m", "build", "--no-isolation",
                             "--outdir", run / "wheels", project], ROOT, run / "build.log")
    wheel = next((run / "wheels").glob("*.whl"))
    unpacked = run / "unpacked"
    with zipfile.ZipFile(wheel) as archive:
        for name in archive.namelist():
            if name.startswith("standard/") and not name.endswith("/"):
                if ".." in Path(name).parts:
                    raise ValueError("unsafe wheel member")
                target = unpacked / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.read(name))
    consumer_manifest = sorust.verify_artifacts(unpacked / "standard")
    (run / "exported").mkdir()
    bundle = sorust.export_artifacts(run / "exported/standard", package_dir=unpacked / "standard")
    sorust.export_artifacts(run / "shared-kernel")
    runtime = run / "runtime"
    venv.EnvBuilder(with_pip=True, symlinks=False).create(runtime)
    python = runtime / "bin/python"
    execute([python, "-I", "-m", "pip", "install", "--no-index", "--no-deps",
             "--disable-pip-version-check", wheel], ROOT, run / "install.log")
    env = dict(os.environ, PATH=str(runtime / "bin"))
    env.pop("PYTHONPATH", None)
    missing = subprocess.run([str(python), "-I", "-c",
                              "import sys;sys.path.insert(0,sys.argv[1]);import standard.nl_dsl_llm",
                              str(run / "exported")], cwd=ROOT, env=env, text=True, capture_output=True, timeout=60)
    (run / "bare-export.log").write_text(missing.stdout + missing.stderr)
    assert missing.returncode != 0 and "FileNotFoundError" in missing.stderr and "semantic-profile.json" in missing.stderr
    with (bundle / "semantic-profile.json").open("xb") as sidecar:
        sidecar.write(inputs["standard/semantic-profile.json"])
    rust_artifact = next(x for x in manifest["artifacts"] if x["kind"] == "rust-cdylib")
    module_artifact = next(x for x in consumer_manifest["artifacts"] if x["path"].startswith("nl_dsl_llm."))
    write_json(run / "run.json", {"number": args.number, "rustArtifact": rust_artifact,
                                  "profileSha256": digest(inputs["standard/semantic-profile.json"]),
                                  "moduleHashes": {"source": digest(inputs["standard/nl_dsl_llm.py"]),
                                                   "wheel": module_artifact["sha256"], "exported": module_artifact["sha256"]}})
    observations = {}
    for mode in ["source", "wheel", "exported"]:
        execute([python, "-I", Path(__file__).resolve(), "--worker", mode, "--run-root", run,
                 "--report", run / f"{mode}.json"], ROOT, run / f"{mode}.log", environment=env)
        observations[mode] = json.loads((run / f"{mode}.json").read_text())
    parity_sha = compare(observations)
    rust_source = run / "reuse.rs"
    rust_source.write_text('''fn main() {
    println!("{} {} {}", sorust_kernel::count_ascii_tokens(b"show open tickets"),
        sorust_kernel::count_ascii_tokens("pokaż otwarte zadania".as_bytes()),
        sorust_kernel::count_ascii_tokens(b""));
}
''')
    execute(["rustc", "--edition=2021", "-C", "panic=abort", rust_source, "--extern",
             "sorust_kernel=" + str(args.rust_rlib.resolve()), "-o", run / "reuse"], ROOT, run / "rlib-build.log")
    execute([run / "reuse"], ROOT, run / "rlib-run.log", environment=env)
    assert (run / "rlib-run.log").read_text().strip() == "3 3 0"
    speeds = {name: observations["source"]["measurements"][name]["median_seconds"] /
              observations["wheel"]["measurements"][name]["median_seconds"]
              for name in ["parse", "dsl_roundtrip", "bridge"]}
    result = {"schema": "sorust.nl-dsl-pilot/v1", "sorustRevision": own_revision,
              "scriptSha256": digest(Path(__file__).read_bytes()), "consumerRevision": args.revision,
              "consumerFiles": {name: digest(data) for name, data in inputs.items()},
              "sorustWheelSha256": digest(args.sorust_wheel.read_bytes()), "consumerWheelSha256": digest(wheel.read_bytes()),
              "consumerManifest": consumer_manifest, "sharedRustManifest": manifest,
              "buildSeconds": build_seconds, "observationsSha256": parity_sha,
              "inputs": {"queries": QUERIES, "commands": COMMANDS, "readQueries": READ_QUERIES},
              "modes": observations, "wheelSpeedup": speeds,
              "rlibReuse": {"sha256": digest(args.rust_rlib.read_bytes()), "rustc": rustc, "panic": "abort", "result": [3, 3, 0]},
              "bareExportMissingConsumerResource": True, "explicitSidecarSha256": digest(inputs["standard/semantic-profile.json"]),
              "method": "Separate minimal-runtime processes, 7 warmed timeit series per mode, list/result creation included. FFI includes UTF-8 encoding, joining, lengths and owned outputs. Preparation/build/import excluded. Fixed fixture-derived corpus, no CPU affinity, no production/LLM traffic or speed threshold. cProfile covers parser calls; native internals are opaque. Unicode split and Rust ASCII counting remain different contracts."}
    write_json(run / "result.json", result)
    print(json.dumps({"report": str(run / "result.json"), "wheelSpeedup": speeds,
                      "conformancePerMode": {k: len(v["conformanceTests"]) for k, v in observations.items()}}, indent=2))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--consumer-root", type=Path)
    parser.add_argument("--revision", default=REVISION)
    parser.add_argument("--sorust-wheel", type=Path)
    parser.add_argument("--rust-rlib", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--number", type=int, default=60)
    parser.add_argument("--worker", choices=["source", "wheel", "exported"], help=argparse.SUPPRESS)
    parser.add_argument("--run-root", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--report", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.worker:
        if args.run_root is None or args.report is None:
            parser.error("worker requires run-root and report")
        return worker(args.run_root, args.worker, args.report)
    if any(x is None for x in [args.consumer_root, args.sorust_wheel, args.rust_rlib, args.output]):
        parser.error("consumer-root, sorust-wheel, rust-rlib and output are required")
    if not 1 <= args.number <= 10000:
        parser.error("number must be between 1 and 10000")
    return pilot(args)


if __name__ == "__main__":
    main()
