"""Brute-force k-NN over `ids.txt`, used as a correctness baseline for the
grid-accelerated implementations in `sp_queries.py` and `knn_grid.py`.

Usage: python3 knn_bruteforce.py <k> <x> <y>
"""

from __future__ import annotations

import argparse
import heapq
import math
import time
from typing import List, Tuple


def euclidean(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def k_nearest_bruteforce(
    k: int, query: Tuple[float, float], ids_path: str = "ids.txt"
) -> List[Tuple[float, str]]:
    # use a max-heap of size k (store negative distances)
    heap: List[Tuple[float, str]] = []
    with open(ids_path, "r", encoding="utf-8") as fh:
        for line in fh:
            parts = line.split()
            if len(parts) < 3:
                continue
            id_str = parts[0]
            x_val = float(parts[1])
            y_val = float(parts[2])
            dist = euclidean(query, (x_val, y_val))
            if len(heap) < k:
                heapq.heappush(heap, (-dist, id_str))
            else:
                if -heap[0][0] > dist:
                    heapq.heapreplace(heap, (-dist, id_str))
    # convert to list sorted ascending by distance
    result = [(-d, id_s) for (d, id_s) in heap]
    result.sort()
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Brute-force k-NN using ids.txt")
    parser.add_argument("k", type=int)
    parser.add_argument("x", type=float)
    parser.add_argument("y", type=float)
    args = parser.parse_args()

    query = f"({args.x}, {args.y})"
    print(f"Scanning ids.txt for {args.k} nearest neighbour(s) of {query} ...")
    start = time.time()
    results = k_nearest_bruteforce(args.k, (args.x, args.y))
    elapsed_ms = (time.time() - start) * 1000

    print(f"{'rank':>4}  {'id':>8}  {'distance':>12}")
    for rank, (dist, id_str) in enumerate(results, start=1):
        print(f"{rank:>4}  {id_str:>8}  {dist:12.6f}")

    print(
        f"\nFound {len(results)}/{args.k} requested neighbour(s) in {elapsed_ms:.2f} ms"
    )


if __name__ == "__main__":
    main()
