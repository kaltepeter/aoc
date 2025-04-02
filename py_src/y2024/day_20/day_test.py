import os
from pathlib import Path

import pytest
from .day import a_star, part_1, part_2, process_input

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    grid, start, end = example_data
    assert len(grid) == 15
    assert len(grid[0]) == 15
    assert start == (1, 3)
    assert end == (5, 7)


def test_a_star(example_data):
    grid, start, end = example_data
    path = a_star(start, end, grid)
    assert len(path) - 1 == 84 # -1 for start


def test_part_1(example_data):
    assert part_1(example_data, 2) == 44


def test_part_2(example_data):
    assert part_2(example_data, 50) == 285
