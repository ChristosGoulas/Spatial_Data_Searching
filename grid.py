"""Create a simple 10x10 spatial grid index from a list of points.

This script reads Beijing_restaurants.txt, writes `ids.txt` (ID + coords),
and generates `grid.grd` (concatenated records) and `grid.dir` (metadata with
cell offsets and counts).
"""

from __future__ import annotations

import argparse
import time
from typing import List, Tuple, Dict

Point = Tuple[float, float]


def read_points(path: str) -> List[Point]:
    """Read points from a whitespace-separated file, skipping header.

    Each data line is expected to contain at least two numeric values (x y).
    Returns list of (x, y).
    """
    points: List[Point] = []
    with open(path, "r", encoding="utf-8") as fh:
        # skip header if present
        _ = fh.readline()
        for line in fh:
            parts = line.strip().split()
            if len(parts) < 2:
                continue
            x_val = float(parts[0])
            y_val = float(parts[1])
            points.append((x_val, y_val))
    return points


def compute_bounds(points: List[Point]) -> Tuple[float, float, float, float]:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), max(xs), min(ys), max(ys)


def build_grid(
    points: List[Point], dimension: int = 10
) -> Tuple[List[List[List[str]]], List[float], List[float]]:
    """Partition points into a `dimension x dimension` grid.

    Returns (cells, x_edges, y_edges) where cells[i][j] is a list of record lines.
    """
    x_min, x_max, y_min, y_max = compute_bounds(points)
    x_step = (x_max - x_min) / dimension
    y_step = (y_max - y_min) / dimension

    x_edges = [round(x_min + i * x_step, 6) for i in range(dimension + 1)]
    y_edges = [round(y_min + i * y_step, 6) for i in range(dimension + 1)]

    cells: List[List[List[str]]] = [
        [[] for _ in range(dimension)] for _ in range(dimension)
    ]

    # Assign points to cells
    for idx, (x, y) in enumerate(points, start=1):
        # find x index
        xi = next(
            (i - 1 for i in range(1, dimension + 1) if x <= x_edges[i]), dimension - 1
        )
        yi = next(
            (j - 1 for j in range(1, dimension + 1) if y <= y_edges[j]), dimension - 1
        )
        record = f"{idx} {x:.6f} {y:.6f}"
        cells[xi][yi].append(record)

    return cells, x_edges, y_edges


def write_index(
    cells: List[List[List[str]]],
    x_edges: List[float],
    y_edges: List[float],
    grd_path: str = "grid.grd",
    dir_path: str = "grid.dir",
) -> None:
    """Write `grid.grd` and `grid.dir`. Offsets are byte offsets into `grid.grd`."""
    dimension = len(cells)
    # write grd and capture offsets
    offsets: Dict[Tuple[int, int], Tuple[int, int]] = {}
    total_chars = 0
    with open(grd_path, "w", encoding="utf-8") as grd_fh:
        for i in range(dimension):
            for j in range(dimension):
                bucket = cells[i][j]
                if not bucket:
                    continue
                offsets[(i, j)] = (grd_fh.tell(), len(bucket))
                for record in bucket:
                    total_chars += grd_fh.write(record + "\n")

    # write directory file: bounds then per-cell info
    x_min, x_max = x_edges[0], x_edges[-1]
    y_min, y_max = y_edges[0], y_edges[-1]
    with open(dir_path, "w", encoding="utf-8") as dir_fh:
        dir_fh.write(f"{x_min:.6f} {x_max:.6f} {y_min:.6f} {y_max:.6f}\n")
        for (i, j), (offset, count) in offsets.items():
            dir_fh.write(f"{i} {j} {offset} {count}\n")


def write_ids(points: List[Point], out_path: str = "ids.txt") -> None:
    with open(out_path, "w", encoding="utf-8") as fh:
        for idx, (x, y) in enumerate(points, start=1):
            fh.write(f"{idx} {x:.6f} {y:.6f}\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a simple 10x10 spatial grid index from a points file."
    )
    parser.add_argument(
        "input", nargs="?", default="Beijing_restaurants.txt", help="input points file"
    )
    parser.add_argument(
        "--dimension", "-d", type=int, default=10, help="grid dimension (default 10)"
    )
    args = parser.parse_args()

    start = time.time()
    points = read_points(args.input)
    if not points:
        print(f"No points found in '{args.input}'; exiting")
        return

    cells, x_edges, y_edges = build_grid(points, dimension=args.dimension)
    write_ids(points)
    write_index(cells, x_edges, y_edges)
    elapsed_ms = (time.time() - start) * 1000

    occupied = [len(bucket) for row in cells for bucket in row if bucket]
    x_min, x_max, y_min, y_max = compute_bounds(points)
    total_cells = args.dimension**2

    print(f"Indexed {len(points):,} points from '{args.input}' in {elapsed_ms:.1f} ms")
    dim = args.dimension
    print(f"  Grid size:        {dim} x {dim} ({len(occupied)}/{total_cells} occupied)")
    print(
        f"  Bounding box:     x=[{x_min:.6f}, {x_max:.6f}] y=[{y_min:.6f}, {y_max:.6f}]"
    )
    if occupied:
        avg = sum(occupied) / len(occupied)
        print(
            f"  Points per cell:  avg={avg:.1f} max={max(occupied)} min={min(occupied)}"
        )
    print("  Output files:     ids.txt, grid.grd, grid.dir")


if __name__ == "__main__":
    main()
