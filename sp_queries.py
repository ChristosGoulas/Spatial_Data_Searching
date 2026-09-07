"""Range query using the grid index (grid.dir + grid.grd).

Usage: python3 sp_queries.py <x_low> <x_high> <y_low> <y_high>
"""

from __future__ import annotations

import argparse
import time
from typing import Dict, List, Tuple


def load_grid_dir(
    path: str = "grid.dir",
) -> Tuple[float, float, float, float, Dict[Tuple[int, int], Tuple[int, int]]]:
    with open(path, "r", encoding="utf-8") as fh:
        first = fh.readline().split()
        x_min, x_max, y_min, y_max = map(float, first)
        grid: Dict[Tuple[int, int], Tuple[int, int]] = {}
        for line in fh:
            parts = line.split()
            if len(parts) < 4:
                continue
            i, j, offset, count = (
                int(parts[0]),
                int(parts[1]),
                int(parts[2]),
                int(parts[3]),
            )
            grid[(i, j)] = (offset, count)
    return x_min, x_max, y_min, y_max, grid


def edges(
    x_min: float, x_max: float, y_min: float, y_max: float, dimension: int = 10
) -> Tuple[List[float], List[float]]:
    x_step = (x_max - x_min) / dimension
    y_step = (y_max - y_min) / dimension
    x_edges = [round(x_min + i * x_step, 6) for i in range(dimension + 1)]
    y_edges = [round(y_min + i * y_step, 6) for i in range(dimension + 1)]
    return x_edges, y_edges


def find_cell_index(value: float, edges_list: List[float]) -> int:
    # return index of cell (0-based)
    for i in range(1, len(edges_list)):
        if value <= edges_list[i]:
            return i - 1
    return len(edges_list) - 2


def range_query(
    x_low: float,
    x_high: float,
    y_low: float,
    y_high: float,
    grid_dir: str = "grid.dir",
    grd_path: str = "grid.grd",
    dimension: int = 10,
) -> List[Tuple[int, int, str, float, float]]:
    """Return every record whose (x, y) falls inside the given box.

    Each result is `(cell_x, cell_y, id, x, y)`.
    """
    x_min, x_max, y_min, y_max, grid = load_grid_dir(grid_dir)
    x_edges, y_edges = edges(x_min, x_max, y_min, y_max, dimension)

    xl = find_cell_index(x_low, x_edges)
    xh = find_cell_index(x_high, x_edges) + 1
    yl = find_cell_index(y_low, y_edges)
    yh = find_cell_index(y_high, y_edges) + 1

    results: List[Tuple[int, int, str, float, float]] = []
    with open(grd_path, "r", encoding="utf-8") as grd:
        for xi in range(xl, xh):
            for yi in range(yl, yh):
                key = (xi, yi)
                if key not in grid:
                    continue
                offset, count = grid[key]
                grd.seek(offset)
                for _ in range(count):
                    parts = grd.readline().split()
                    if len(parts) < 3:
                        continue
                    id_str, x_val, y_val = parts[0], float(parts[1]), float(parts[2])
                    if x_low <= x_val <= x_high and y_low <= y_val <= y_high:
                        results.append((xi, yi, id_str, x_val, y_val))
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Range query against grid index")
    parser.add_argument("x_low", type=float)
    parser.add_argument("x_high", type=float)
    parser.add_argument("y_low", type=float)
    parser.add_argument("y_high", type=float)
    args = parser.parse_args()

    box = f"x=[{args.x_low}, {args.x_high}]  y=[{args.y_low}, {args.y_high}]"
    print(f"Searching box {box} ...")
    start = time.time()
    results = range_query(args.x_low, args.x_high, args.y_low, args.y_high)
    elapsed_ms = (time.time() - start) * 1000

    print(f"{'cell':>8}  {'id':>8}  {'x':>12}  {'y':>12}")
    for xi, yi, id_str, x_val, y_val in results:
        print(f"{f'({xi},{yi})':>8}  {id_str:>8}  {x_val:12.6f}  {y_val:12.6f}")

    print(f"\nFound {len(results)} point(s) in {elapsed_ms:.2f} ms")


if __name__ == "__main__":
    main()
