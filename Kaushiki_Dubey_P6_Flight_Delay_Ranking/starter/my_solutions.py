"""Four handwritten sorting techniques for P6 Flight Delay Ranking.

Each function returns flight IDs in descending arrival-delay order. Equal
delays retain their original CSV order. No built-in sorting routine is used.
"""


def _before(inst, left_index, right_index, stats=None):
    """Return True when left belongs before right in the required output."""
    if stats is not None:
        stats["comparisons"] += 1
    left_delay = inst["delay"][left_index]
    right_delay = inst["delay"][right_index]
    return left_delay > right_delay or (
        left_delay == right_delay and left_index < right_index
    )


def solve_insertion(inst, stats=None):
    """Stable insertion sort, worst delay first."""
    if stats is None:
        stats = {"comparisons": 0, "writes": 0}
    order = list(range(inst["n"]))
    for i in range(1, len(order)):
        current = order[i]
        j = i - 1
        while j >= 0:
            if not _before(inst, current, order[j], stats):
                break
            order[j + 1] = order[j]
            stats["writes"] += 1
            j -= 1
        order[j + 1] = current
        stats["writes"] += 1
    return [inst["ids"][i] for i in order]


def solve_merge(inst, stats=None):
    """Stable top-down mergesort, worst delay first."""
    if stats is None:
        stats = {"comparisons": 0, "writes": 0}
    order = list(range(inst["n"]))
    temp = [0] * inst["n"]

    def merge_sort(lo, hi):
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        merge_sort(lo, mid)
        merge_sort(mid, hi)
        left, right, out = lo, mid, lo
        while left < mid and right < hi:
            # Taking the left item on equality preserves stability.
            if _before(inst, order[left], order[right], stats):
                temp[out] = order[left]
                left += 1
            else:
                temp[out] = order[right]
                right += 1
            stats["writes"] += 1
            out += 1
        while left < mid:
            temp[out] = order[left]
            stats["writes"] += 1
            left += 1
            out += 1
        while right < hi:
            temp[out] = order[right]
            stats["writes"] += 1
            right += 1
            out += 1
        for k in range(lo, hi):
            order[k] = temp[k]
            stats["writes"] += 1

    merge_sort(0, len(order))
    return [inst["ids"][i] for i in order]


def solve_heap(inst, stats=None):
    """In-place heapsort with the original position as a stability tie-break."""
    if stats is None:
        stats = {"comparisons": 0, "writes": 0}
    order = list(range(inst["n"]))

    def comes_after(left_index, right_index):
        # A max-heap uses the item that belongs later in the final order.
        return _before(inst, right_index, left_index, stats)

    def swap(a, b):
        order[a], order[b] = order[b], order[a]
        stats["writes"] += 2

    def sift_down(root, end):
        while True:
            child = 2 * root + 1
            if child > end:
                return
            if child + 1 <= end and comes_after(order[child + 1], order[child]):
                child += 1
            if not comes_after(order[child], order[root]):
                return
            swap(root, child)
            root = child

    n = len(order)
    for root in range(n // 2 - 1, -1, -1):
        sift_down(root, n - 1)
    for end in range(n - 1, 0, -1):
        swap(0, end)
        sift_down(0, end - 1)
    return [inst["ids"][i] for i in order]


def solve_counting(inst, stats=None):
    """Stable descending counting sort with a shifted integer key range."""
    if stats is None:
        stats = {"comparisons": 0, "writes": 0}
    n = inst["n"]
    if n == 0:
        return []
    delays = inst["delay"]
    minimum = delays[0]
    maximum = delays[0]
    for value in delays[1:]:
        if value < minimum:
            minimum = value
        if value > maximum:
            maximum = value
    counts = [0] * (maximum - minimum + 1)
    for value in delays:
        counts[value - minimum] += 1
    starts = [0] * len(counts)
    position = 0
    for bucket in range(len(counts) - 1, -1, -1):
        starts[bucket] = position
        position += counts[bucket]
    order = [0] * n
    # Forward traversal preserves file order within every delay bucket.
    for original_index, value in enumerate(delays):
        bucket = value - minimum
        order[starts[bucket]] = original_index
        starts[bucket] += 1
        stats["writes"] += 1
    return [inst["ids"][i] for i in order]


TECHNIQUES = {
    "insertion": solve_insertion,
    "merge": solve_merge,
    "heap": solve_heap,
    "counting": solve_counting,
}
