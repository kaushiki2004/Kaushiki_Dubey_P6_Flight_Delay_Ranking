# Office Discussion Preparation

Kaushiki Dubey should practice answering these without reading.

## Thirty-second problem statement

The program receives flight records in file order and returns their IDs from the largest arrival delay to the smallest. Equal delays must keep file order, so all four algorithms produce one deterministic result.

## Key explanations

### Insertion sort

Invariant: before iteration `i`, positions `0` through `i - 1` are already ranked. The algorithm shifts only records with a strictly smaller delay. It does not shift an equal-delay record, so ties remain stable.

### Heapsort

Ordinary heapsort is unstable. This implementation treats the original row index as a secondary key. The desired key is descending delay followed by ascending original position, which makes every record's order unique.

### Mergesort

The algorithm recursively sorts each half and merges them. When delays tie, the merge selects the record from the left half first. That preserves the original order.

### Counting sort

The delay values occupy a small integer range. The algorithm counts each value, calculates the starting position for every delay bucket in descending order, and scans the input forward when placing records. The forward pass preserves ties.

## Complexity summary

| Algorithm | Time | Extra working space | Stable |
|---|---:|---:|---|
| Insertion | Best Θ(n), average/worst Θ(n²) | Θ(1), excluding required output | Yes |
| Heapsort | Θ(n log n) | Θ(1), excluding required output/index array | Tie-break makes required order deterministic |
| Mergesort | Θ(n log n) | Θ(n) | Yes |
| Counting | Θ(n + R) | Θ(n + R) | Yes |

## Likely questions

1. Why not use `sorted()`? The assignment studies the algorithms themselves and explicitly forbids library sorting inside the techniques.
2. Why does insertion sort improve on nearly sorted data? It performs work proportional to the number of inversions, so it makes few shifts when most records already occupy the right region.
3. Why is heap construction Θ(n), not Θ(n log n)? Most nodes sit near the leaves and move only a short distance during bottom-up heap construction.
4. Why can counting sort beat the comparison lower bound? It uses integer keys in a bounded range and does not determine order through pairwise key comparisons.
5. What happens with 64-bit timestamps? The possible range becomes far too large for a count array, so mergesort becomes the practical choice.
6. What small change might the instructor request? Be prepared to reverse the order, add a secondary carrier key, print operation counts, or return full rows instead of IDs.

## Demonstration sequence

1. Run the seven edge-case tests.
2. Run the supplied harness on the small dataset.
3. Trace `[5, 20, 5, 20, 5]` and explain why the output is `F1, F3, F0, F2, F4`.
4. Show the results tables and connect each curve to its expected complexity.
5. State the recommendation: counting sort for this bounded delay range, mergesort when the key range may be large, insertion sort for small or nearly ranked inputs, and heapsort when predictable time and low auxiliary memory matter.
