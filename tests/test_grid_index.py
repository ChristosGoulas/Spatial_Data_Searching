"""Correctness tests: grid-accelerated queries must agree with brute force."""

import random

import pytest

from grid import build_grid, write_ids, write_index
from knn_bruteforce import k_nearest_bruteforce
from knn_grid import k_nearest_grid
from sp_queries import range_query

DIMENSION = 5


@pytest.fixture()
def dataset(tmp_path):
    random.seed(42)
    points = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(200)]

    ids_path = tmp_path / "ids.txt"
    grd_path = tmp_path / "grid.grd"
    dir_path = tmp_path / "grid.dir"

    cells, x_edges, y_edges = build_grid(points, dimension=DIMENSION)
    write_ids(points, out_path=str(ids_path))
    write_index(cells, x_edges, y_edges, grd_path=str(grd_path), dir_path=str(dir_path))

    return points, str(ids_path), str(grd_path), str(dir_path)


def test_range_query_matches_bruteforce(dataset):
    points, ids_path, grd_path, dir_path = dataset
    x_low, x_high, y_low, y_high = 20.0, 60.0, 10.0, 50.0

    expected_ids = {
        idx
        for idx, (x, y) in enumerate(points, start=1)
        if x_low <= x <= x_high and y_low <= y <= y_high
    }

    results = range_query(
        x_low,
        x_high,
        y_low,
        y_high,
        grid_dir=dir_path,
        grd_path=grd_path,
        dimension=DIMENSION,
    )
    found_ids = {int(id_str) for _, _, id_str, _, _ in results}

    assert found_ids == expected_ids


def test_knn_grid_matches_bruteforce(dataset):
    points, ids_path, grd_path, dir_path = dataset
    query = (55.0, 42.0)
    k = 5

    expected = k_nearest_bruteforce(k, query, ids_path=ids_path)
    expected_ids = {id_str for _, id_str in expected}

    actual = k_nearest_grid(
        k, *query, grid_dir=dir_path, grd_path=grd_path, dimension=DIMENSION
    )
    actual_ids = {id_str for _, id_str in actual}

    assert len(actual) == k
    assert actual_ids == expected_ids


def test_knn_grid_distances_are_sorted(dataset):
    _, _, grd_path, dir_path = dataset
    results = k_nearest_grid(
        10, 30.0, 30.0, grid_dir=dir_path, grd_path=grd_path, dimension=DIMENSION
    )

    distances = [dist for dist, _ in results]
    assert distances == sorted(distances)
