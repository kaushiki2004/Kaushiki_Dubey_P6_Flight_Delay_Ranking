# P6 Flight Delay Ranking Audit

**Student:** Kaushiki Dubey  
**Responsibility:** Individual completion of Group A and Group B, covering all four algorithms

This project ranks flights from the largest arrival delay to the smallest. Flights with equal delays remain in their original CSV order.

## Algorithms

- Insertion sort
- Heapsort with original-position tie-breaking
- Stable mergesort
- Stable counting sort

## Requirements

- Python 3.10 or newer
- The four sorting techniques use the Python standard library only
- Matplotlib is required only to regenerate the PNG plots

## Run the correctness checks

From the `starter` folder:

```bash
python run_checks.py my_solutions.py
python -m unittest -v test_edge_cases.py
```

## Reproduce the experiments

```bash
python benchmark.py --repeats 5
python make_plots.py
```

The benchmark writes CSV results and environment details to `results/`. The plotting script writes labelled PNG figures to `results/figures/`.

## Folder contents

- `starter/my_solutions.py`: four handwritten algorithms
- `starter/test_edge_cases.py`: focused unit tests
- `starter/benchmark.py`: timings, operation counts, and memory measurements
- `starter/make_plots.py`: reproducible plots
- `data/`: supplied synthetic datasets, manifest, and generator
- `results/`: measured CSV results and figures
- `report/`: final report and office-discussion notes
- `slides/`: presentation
- `flight_delay_race_demo.html`: interactive demo of the four algorithms and the benchmark results

The report opens with the required one-page recommendation comparing all four algorithms.

## Submission steps

1. Create or open the shared GitHub repository required by the course.
2. Add the complete `Kaushiki_Dubey_P6_Flight_Delay_Ranking` folder to the repository.
3. Commit and push all files, including the data, source code, results, report, and slides.
4. Open the repository while signed out or in a private browser window to confirm the instructor can access it.
5. Submit the GitHub repository link through the course's designated submission channel before 11:59 p.m. on November 22, 2026.
6. Bring the repository, code, report, and presentation to the office discussion on November 23 or 24.

## Interactive demo

`flight_delay_race_demo.html` is a self-contained page. Open it in any browser; it works offline, and web fonts load only when a connection is available. It lets you:

- race the four algorithms side by side with live comparison and write counters,
- compare plain heapsort with the original-position tie-break on the same flights,
- explore the results in `results/` as interactive charts.

The page re-implements the four algorithms in JavaScript for visualization only. The graded implementation is `starter/my_solutions.py`, and every reported measurement comes from the Python benchmark.

## Data source

The assignment supplied synthetic datasets generated from fixed random seeds. The package includes `generate_data.py` so the data can be reproduced. No external dataset was required.

## Assistance disclosure

AI assistance supported planning, code review, document drafting, and presentation preparation. The student reviewed the algorithms, tests, measurements, and explanations and remains responsible for being able to trace and modify the code during the office discussion. AI assistance also supported the interactive demo (`flight_delay_race_demo.html`).
