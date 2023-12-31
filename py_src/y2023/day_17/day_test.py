import os
from pathlib import Path

import pytest
from .day import (
    part_1,
    part_2,
    process_input,
    HeatLossGrid,
    WEST,
    EAST,
    NORTH,
    SOUTH,
    START,
)

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert next(example_data) == [
        [2, 4, 1, 3, 4, 3, 2, 3, 1, 1, 3, 2, 3],
        [3, 2, 1, 5, 4, 5, 3, 5, 3, 5, 6, 2, 3],
        [3, 2, 5, 5, 2, 4, 5, 6, 5, 4, 2, 5, 4],
        [3, 4, 4, 6, 5, 8, 5, 8, 4, 5, 4, 5, 2],
        [4, 5, 4, 6, 6, 5, 7, 8, 6, 7, 5, 3, 6],
        [1, 4, 3, 8, 5, 9, 8, 7, 9, 8, 4, 5, 4],
        [4, 4, 5, 7, 8, 7, 6, 9, 8, 7, 7, 6, 6],
        [3, 6, 3, 7, 8, 7, 7, 9, 7, 9, 6, 5, 3],
        [4, 6, 5, 4, 9, 6, 7, 9, 8, 6, 8, 8, 7],
        [4, 5, 6, 4, 6, 7, 9, 9, 8, 6, 4, 5, 3],
        [1, 2, 2, 4, 6, 8, 6, 8, 6, 5, 5, 6, 3],
        [2, 5, 4, 6, 5, 4, 8, 8, 8, 7, 7, 3, 5],
        [4, 3, 2, 2, 6, 7, 4, 6, 5, 5, 5, 3, 3],
    ]


def test_heat_loss_grid_add(example_data):
    data = next(example_data)
    rows = len(data)
    cols = len(data[0])
    graph: HeatLossGrid = HeatLossGrid(cols, rows)
    assert graph.add((0, 0), (1, 0)) == (1, 0)
    assert graph.add((0, 0), (0, 1)) == (0, 1)
    assert graph.add((1, 0), (1, 0)) == (2, 0)
    assert graph.add((1, 1), (0, -1)) == (1, 0)


def test_part_1(example_data):
    assert part_1(next(example_data)) == 102


def test_part_2(example_data):
    assert part_2(next(example_data)) == 94
