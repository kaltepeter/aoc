import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input, calc_weight

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))

@pytest.fixture()
def example_data2():
    return process_input(os.path.join(base_path, "example2.txt"))


def test_process_input(example_data):
    map, start, end, max_x, max_y = example_data
    assert start == (1, 13)
    assert end == (13, 1)
    assert len(map.nodes) == 104
    assert max_x == 15
    assert max_y == 15


@pytest.mark.parametrize(
    "start, end, edge_data, expected_weight",
    [
        ((1,13), (1,13), {"direction": (1, 0)}, 0),
        ((1, 13), (2, 13), {"direction": (1, 0)}, 1),
        ((1, 13), (1, 12), {"direction": (1, 0)}, 1001),
        ((1, 13), (1, 12), {"direction": (0, -1)}, 1),
        ((5, 5), (5, 6), {"direction": (0, -1)}, 2001),
        ((5, 5), (4, 5), {"direction": (0, -1)}, 1001),
        ((5, 5), (6, 5), {"direction": (0, -1)}, 1001),
    ],
)
def test_calc_weight(start, end, edge_data, expected_weight):
    assert calc_weight(start, end, edge_data) == expected_weight


def test_part_1(example_data):
    assert part_1(example_data) == 7036 


def test_part_1_example2(example_data2):
    assert part_1(example_data2) == 11048 


def test_part_2(example_data):
    assert part_2(example_data) == 45


def test_part_2_example2(example_data2):
    assert part_2(example_data2) == 64