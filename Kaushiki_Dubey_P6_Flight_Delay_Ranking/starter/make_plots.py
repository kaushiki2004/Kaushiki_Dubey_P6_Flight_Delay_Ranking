"""Create labelled figures from benchmark CSV files."""

import csv
import os

import matplotlib.pyplot as plt


HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.abspath(os.path.join(HERE, "..", "results"))
FIGURES = os.path.join(RESULTS, "figures")
COLORS = {
    "insertion": "#C44E52",
    "heap": "#8172B2",
    "merge": "#4C72B0",
    "counting": "#55A868",
}


def read_csv(name):
    with open(os.path.join(RESULTS, name), newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def save(name):
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES, name), dpi=180, bbox_inches="tight")
    plt.close()


def scaling_plot():
    rows = read_csv("scaling_results.csv")
    for method in COLORS:
        selected = [row for row in rows if row["method"] == method]
        if not selected:
            continue
        plt.plot([int(r["n"]) for r in selected],
                 [float(r["median_seconds"]) for r in selected],
                 marker="o", linewidth=2, label=method.title(), color=COLORS[method])
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Number of flight records n")
    plt.ylabel("Median running time (seconds)")
    plt.title("Running time by input size")
    plt.grid(True, which="both", alpha=0.25)
    plt.legend()
    save("time_vs_n.png")


def order_plot():
    rows = read_csv("input_order_results.csv")
    labels = ["schedule", "nearly_sorted", "reversed"]
    methods = list(COLORS)
    x = range(len(labels))
    width = 0.18
    for offset, method in enumerate(methods):
        values = []
        for label in labels:
            row = next(r for r in rows if r["method"] == method and r["dataset"] == label)
            values.append(float(row["median_seconds"]))
        positions = [value + (offset - 1.5) * width for value in x]
        plt.bar(positions, values, width=width, label=method.title(), color=COLORS[method])
    plt.xticks(list(x), ["Schedule", "Nearly sorted", "Reversed"])
    plt.yscale("log")
    plt.ylabel("Median running time (seconds, log scale)")
    plt.title("Effect of file order at n = 10,000")
    plt.grid(True, axis="y", alpha=0.25)
    plt.legend()
    save("time_by_input_order.png")


def comparisons_plot():
    rows = read_csv("scaling_results.csv")
    for method in ("insertion", "heap", "merge"):
        selected = [row for row in rows if row["method"] == method]
        plt.plot([int(r["n"]) for r in selected],
                 [int(r["comparisons"]) for r in selected],
                 marker="o", linewidth=2, label=method.title(), color=COLORS[method])
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Number of flight records n")
    plt.ylabel("Key comparisons")
    plt.title("Comparison growth")
    plt.grid(True, which="both", alpha=0.25)
    plt.legend()
    save("comparisons_vs_n.png")


def range_plot():
    rows = read_csv("key_range_results.csv")
    for method in ("merge", "counting"):
        selected = [row for row in rows if row["method"] == method]
        ranges = [int(r["dataset"].split("=")[1]) for r in selected]
        times = [float(r["median_seconds"]) for r in selected]
        plt.plot(ranges, times, marker="o", linewidth=2,
                 label=method.title(), color=COLORS[method])
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Integer key range R")
    plt.ylabel("Median running time (seconds)")
    plt.title("Effect of key range at n = 50,000")
    plt.grid(True, which="both", alpha=0.25)
    plt.legend()
    save("time_by_key_range.png")


def memory_plot():
    rows = read_csv("scaling_results.csv")
    selected = [row for row in rows if int(row["n"]) == 100000]
    methods = [row["method"] for row in selected]
    mib = [int(row["peak_bytes"]) / 1024 / 1024 for row in selected]
    plt.bar([m.title() for m in methods], mib, color=[COLORS[m] for m in methods])
    plt.ylabel("Peak traced memory (MiB)")
    plt.title("Measured peak memory at n = 100,000")
    plt.grid(True, axis="y", alpha=0.25)
    save("peak_memory.png")


def main():
    os.makedirs(FIGURES, exist_ok=True)
    scaling_plot()
    order_plot()
    comparisons_plot()
    range_plot()
    memory_plot()


if __name__ == "__main__":
    main()
