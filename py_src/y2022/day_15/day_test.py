import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert example_data.beacons == set(
        [(-2, 15), (10, 16), (15, 3), (10, 16), (2, 10), (25, 17), (21, 22), (15, 3)]
    )
    assert len(example_data.sensors) == 14
    assert example_data.sensors[(2, 18)] == {"nearest_beacon": (-2, 15), "distance": 7}
    # assert example_data.lowest_x == -2
    # assert example_data.highest_x == 25
    # assert example_data.lowest_y == 0
    # assert example_data.highest_y == 22


def test_part_1(example_data):
    assert part_1(example_data, 10) == 26


def test_part_2(example_data):
    assert part_2(example_data) == 0
