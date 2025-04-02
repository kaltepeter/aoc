import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input, Coord

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


# def test_process_input(example_data):
#     assert example_data.width == 8
#     assert example_data.height == 8
#     cell_1 = example_data.lava_map.get((0, 0))
#     assert cell_1 == 8
#     assert example_data.passable((0, 0), (1, 0)) == True
#     assert example_data.passable((0, 0), (0, 1)) == False
#     assert example_data.neighbors((0, 0)) == [(1, 0), (0, 1)]
#     assert example_data.trail_heads == [(2, 0), (4, 0), (4, 2), (6, 4), (2, 5), (5, 5), (0, 6), (6, 6), (1, 7)]


def test_part_1(example_data):
    assert part_1(example_data) == 36 


def test_part_2(example_data):
    assert part_2(example_data) == 81
