"""Compare installed public/prepared scalar APIs and report preparation cost."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import platform
import re
import statistics
import sys
import timeit

import sorust


def measure(function, number):
    function()
    samples = [value / number for value in timeit.repeat(function, number=number, repeat=7)]
    return {"number": number, "median_seconds": statistics.median(samples), "samples_seconds": samples}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    manifest = sorust.verify_artifacts()
    measurements = []
    preparation = {}
    for backend in ["rust", "compiled-python"]:
        counter = sorust.prepare_ascii_token_counter(backend=backend)
        preparation[backend] = measure(lambda: sorust.prepare_ascii_token_counter(backend=backend), 3)
        for payload, number in [(b"a b", 100), (b"one two " * 8, 100), (b"x y " * 1024, 20)]:
            expected = len(re.findall(rb"[^\x09-\x0d\x20]+", payload))
            assert counter(payload) == sorust.count_ascii_tokens(payload, backend=backend) == expected
            public = measure(lambda: sorust.count_ascii_tokens(payload, backend=backend), number)
            prepared = measure(lambda: counter(payload), number)
            measurements.append({"backend": backend, "bytes": len(payload), "public": public,
                                 "prepared": prepared, "speedup": public["median_seconds"] / prepared["median_seconds"]})
    result = {"schema": "sorust.prepared-counter-benchmark/v1",
              "recordedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "python": sys.version, "platform": platform.platform(), "manifest": manifest,
              "benchmarkSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "preparation": preparation, "measurements": measurements,
              "method": "7 warmed timeit series, public/prepared same-wheel scalar API, normalization and result included. Preparation excludes cold loader cost and is measured separately, outside steady-state. No CPU affinity; small repeated buffers, not nl-* workload evidence or a Rust speedup target."}
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
