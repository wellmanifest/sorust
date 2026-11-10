"""Run against an installed wheel: python -I tests/benchmark_count_many.py."""
import argparse
import datetime
import gc
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import statistics
import sys
import timeit
import time
import tracemalloc

import sorust


def measure_memory():
    payload = b"x y " * 1024
    count = 4096
    expected = count * sorust.count_ascii_tokens(payload)
    sorust.count_ascii_tokens_many([b"warm"])

    def inputs():
        for _ in range(count):
            yield bytes(bytearray(payload))

    modes = {"rust-many": lambda: sum(sorust.count_ascii_tokens_many(inputs()))}
    if hasattr(sorust, "iter_ascii_token_counts"):
        modes["rust-stream"] = lambda: sum(sorust.iter_ascii_token_counts(inputs(), batch_size=256))
    results = {}
    for name, function in modes.items():
        samples = []
        for _ in range(3):
            gc.collect()
            tracemalloc.start()
            try:
                start = time.perf_counter()
                actual = function()
                elapsed = time.perf_counter() - start
                current, peak = tracemalloc.get_traced_memory()
            finally:
                tracemalloc.stop()
            assert actual == expected
            samples.append({"peak_python_bytes": peak, "remaining_python_bytes": current,
                            "seconds": elapsed, "checksum": actual})
        results[name] = {"samples": samples, "median_peak_python_bytes":
                         statistics.median(sample["peak_python_bytes"] for sample in samples)}
    return {"buffers": count, "bytes_per_buffer": len(payload), "batch_size": 256,
            "modes": results, "method": "3 warm-kernel tracemalloc runs; unique bytes via bytes(bytearray(payload)); sum consumes outputs. Python allocation peak, not process RSS or nl-* workload evidence."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--memory", action="store_true", help="also compare eager and bounded generator memory")
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1] / "src/sorust/_compat.py"
    spec = importlib.util.spec_from_file_location("reference", source)
    reference = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reference)
    manifest = sorust.verify_artifacts()
    measurements = []
    for payload, number in [(b"a b", 20), (b"one two " * 8, 5), (b"x y " * 1024, 1)]:
        values = [payload] * 256
        expected = [reference.count_ascii_tokens(value) for value in values]
        functions = {
            "python-reference": lambda: [reference.count_ascii_tokens(value) for value in values],
            "rust-scalar": lambda: [sorust.count_ascii_tokens(value) for value in values],
        }
        if hasattr(sorust, "count_ascii_tokens_many"):
            functions["rust-many"] = lambda: sorust.count_ascii_tokens_many(values)
            functions["compiled-python-many"] = lambda: sorust.count_ascii_tokens_many(values, backend="compiled-python")
        timings = {}
        for name, function in functions.items():
            assert function() == expected
            samples = [sample / number for sample in timeit.repeat(function, number=number, repeat=9)]
            timings[name] = {"median_batch_seconds": statistics.median(samples), "samples_batch_seconds": samples}
        measurements.append({"bytes_per_buffer": len(payload), "buffers": len(values), "number": number,
                             "timings": timings, "rust_many_speedup":
                             timings["rust-scalar"]["median_batch_seconds"] / timings["rust-many"]["median_batch_seconds"]
                             if "rust-many" in timings else None})
    receipt = {
        "schema": "sorust.batch-benchmark/v1",
        "recordedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python": sys.version, "platform": platform.platform(),
        "benchmarkSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "referenceSha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "manifest": manifest, "measurements": measurements,
        "method": "Median of 9 warmed repeats; includes input normalization, joining/arrays and result construction. No CPU affinity; microbenchmark, not nl-* workload evidence.",
    }
    if args.memory:
        receipt["memory"] = measure_memory()
    rendered = json.dumps(receipt, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
