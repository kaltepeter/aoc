import os
from pathlib import Path

import pytest
from .day import part_1, part_2, print_reservoir_map, process_input, str_loc_to_location

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_str_loc_to_location():
    assert str_loc_to_location("498,4") == (498, 4)


def test_process_input(example_data):
    reservoir_map = example_data
    assert sorted(reservoir_map.rocks) == sorted(
        [
            (498, 4),
            (498, 5),
            (498, 6),
            (497, 6),
            (496, 6),
            (503, 4),
            (502, 4),
            (502, 5),
            (502, 6),
            (502, 7),
            (502, 8),
            (502, 9),
            (501, 9),
            (500, 9),
            (499, 9),
            (498, 9),
            (497, 9),
            (496, 9),
            (495, 9),
            (494, 9),
        ]
    )
    assert reservoir_map.lowest_x == 494
    assert reservoir_map.highest_x == 503
    assert reservoir_map.lowest_y == 0
    assert reservoir_map.highest_y == 9


def test_part_1(example_data):
    assert part_1(example_data) == 24


def test_part_2(example_data):
    assert part_2(example_data) == 0
