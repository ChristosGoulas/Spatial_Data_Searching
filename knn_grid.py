"""Grid-accelerated k-nearest-neighbour search (grid.dir + grid.grd).

Starting from the query point's home cell, this expands outward in square
"rings" of cells and stops as soon as `k` candidates have been found *and*
no unvisited ring could possibly contain a closer point.

Usage: python3 knn_grid.py <k> <x> <y>
"""

from __future__ import annotations

import argparse
import heapq
import math
import time
from typing import List, Tuple

from sp_queries import edges, find_cell_index, load_grid_dir


def euclidean(ax: float, ay: float, bx: float, by: float) -> float:
    return math.hypot(ax - bx, ay - by)


def ring_cells(cx: int, cy: int, radius: int, dimension: int) -> List[Tuple[int, int]]:
    """Cells at Chebyshev distance `radius` from (cx, cy), clipped to the grid."""
    if radius == 0:
        return [(cx, cy)]
    cells = []
    for i in range(cx - radius, cx + radius + 1):
        for j in range(cy - radius, cy + radius + 1):
            if max(abs(i - cx), abs(j - cy)) != radius:
                continue
            if 0 <= i < dimension and 0 <= j < dimension:
                cells.append((i, j))
    return cells


def read_cell_records(
    grd_path: str, offset: int, count: int
) -> List[Tuple[str, float, float]]:
    records = []
    with open(grd_path, "r", encoding="utf-8") as grd:
        grd.seek(offset)
        for _ in range(count):
            parts = grd.readline().split()
            if len(parts) < 3:
                continue
            records.append((parts[0], float(parts[1]), float(parts[2])))
    return records


def k_nearest_grid(
    k: int,
    x: float,
    y: float,
    grid_dir: str = "grid.dir",
    grd_path: str = "grid.grd",
    dimension: int = 10,
) -> List[Tuple[float, str]]:
    """Return the `k` nearest points to (x, y), sorted ascending by distance."""
    x_min, x_max, y_min, y_max, grid = load_grid_dir(grid_dir)
    x_edges, y_edges = edges(x_min, x_max, y_min, y_max, dimension)
    cell_width = (x_max - x_min) / dimension
    cell_height = (y_max - y_min) / dimension

    cx = min(max(find_cell_index(x, x_edges), 0), dimension - 1)
    cy = min(max(find_cell_index(y, y_edges), 0), dimension - 1)

    heap: List[Tuple[float, str]] = []  # max-heap of size k via negated distance
    radius = 0
    while radius <= dimension:
        for i, j in ring_cells(cx, cy, radius, dimension):
            if (i, j) not in grid:
                continue
            offset, count = grid[(i, j)]
            for id_str, px, py in read_cell_records(grd_path, offset, count):
                dist = euclidean(x, y, px, py)
                if len(heap) < k:
                    heapq.heappush(heap, (-dist, id_str))
                elif -heap[0][0] > dist:
                    heapq.heapreplace(heap, (-dist, id_str))

        # Closest a point in the next, unvisited ring could possibly be.
        next_ring_min_dist = radius * min(cell_width, cell_height)
        if len(heap) >= k and next_ring_min_dist > -heap[0][0]:
            break
        radius += 1

    return sorted((-dist, id_str) for dist, id_str in heap)


def main() -> None:
    parser = argparse.ArgumentParser(description="Grid-accelerated k-NN query")
    parser.add_argument("k", type=int)
    parser.add_argument("x", type=float)
    parser.add_argument("y", type=float)
    args = parser.parse_args()

    query = f"({args.x}, {args.y})"
    print(f"Searching {args.k} nearest neighbour(s) of {query} via the grid ...")
    start = time.time()
    results = k_nearest_grid(args.k, args.x, args.y)
    elapsed_ms = (time.time() - start) * 1000

    print(f"{'rank':>4}  {'id':>8}  {'distance':>12}")
    for rank, (dist, id_str) in enumerate(results, start=1):
        print(f"{rank:>4}  {id_str:>8}  {dist:12.6f}")

    print(
        f"\nFound {len(results)}/{args.k} requested neighbour(s) in {elapsed_ms:.2f} ms"
    )


if __name__ == "__main__":
    main()
