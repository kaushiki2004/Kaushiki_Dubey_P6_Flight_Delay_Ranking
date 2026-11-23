"""Reproducible benchmarks and operation counts for the P6 report."""

import argparse
import csv
import json
import os
import platform
import statistics
import sys
import time
import tracemalloc

from my_solutions import TECHNIQUES
from problem import load_instance, validate


HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))


def trimmed(inst, n):
    rows = inst["rows"][:n]
    return {
        "n": len(rows),
        "ids": [row[0] for row in rows],
        "delay": [row[5] for row in rows],
        "rows": rows,
    }


def measure(technique_name, inst, repeats):
    technique = TECHNIQUES[technique_name]
    times = []
    solution = None
    for _ in range(repeats):
        start = time.perf_counter()
        solution = technique(inst)
        times.append(time.perf_counter() - start)
    valid, _, message = validate(inst, solution)
    if not valid:
        raise AssertionError(f"{technique_name}: {message}")
    stats = {"comparisons": 0, "writes": 0}
    technique(inst, stats)
    tracemalloc.start()
    technique(inst)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "median_seconds": statistics.median(times),
        "min_seconds": min(times),
        "max_seconds": max(times),
        "comparisons": stats["comparisons"],
        "writes": stats["writes"],
        "peak_bytes": peak,
    }


def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--output", default=os.path.join(HERE, "..", "results"))
    args = parser.parse_args()
    os.makedirs(args.output, exist_ok=True)

    schedule_100k = load_instance(os.path.join(DATA, "flights_n100000_schedule.csv"))
    scale_rows = []
    for n in (100, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000):
        inst = trimmed(schedule_100k, n)
        methods = ["merge", "heap", "counting"]
        if n <= 10000:
            methods.insert(0, "insertion")
        for method in methods:
            result = measure(method, inst, args.repeats)
            scale_rows.append({"experiment": "scale", "dataset": "schedule", "n": n,
                               "method": method, **result})
            print("scale", n, method, result["median_seconds"])
    write_csv(os.path.join(args.output, "scaling_results.csv"), scale_rows)

    order_rows = []
    order_files = {
        "schedule": "flights_n010000_schedule.csv",
        "nearly_sorted": "flights_n010000_nearly_sorted.csv",
        "reversed": "flights_n010000_reversed.csv",
    }
    for label, filename in order_files.items():
        inst = load_instance(os.path.join(DATA, filename))
        for method in TECHNIQUES:
            result = measure(method, inst, args.repeats)
            order_rows.append({"experiment": "input_order", "dataset": label,
                               "n": inst["n"], "method": method, **result})
            print("order", label, method, result["median_seconds"])
    write_csv(os.path.join(args.output, "input_order_results.csv"), order_rows)

    range_rows = []
    base = trimmed(schedule_100k, 50000)
    for width in (11, 101, 961, 10001, 100001):
        delays = [((value + 60) * (width - 1) // 960) for value in base["delay"]]
        inst = {**base, "delay": delays}
        for method in ("merge", "counting"):
            result = measure(method, inst, args.repeats)
            range_rows.append({"experiment": "key_range", "dataset": f"R={width}",
                               "n": inst["n"], "method": method, **result})
            print("range", width, method, result["median_seconds"])
    write_csv(os.path.join(args.output, "key_range_results.csv"), range_rows)

    metadata = {
        "python": sys.version,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "repeats": args.repeats,
        "timer": "time.perf_counter",
        "summary": "Median of repeated runs; tracemalloc peak measured separately.",
    }
    with open(os.path.join(args.output, "environment.json"), "w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2)


if __name__ == "__main__":
    main()
