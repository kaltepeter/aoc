import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input, extract_tuple

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert example_data == {
        1: [(4, 0, 3), (1, 2, 6), (0, 2, 0)],
        2: [(0, 2, 1), (1, 3, 4), (0, 1, 1)],
        3: [(20, 8, 6), (4, 13, 5), (1, 5, 0)],
        4: [(3, 1, 6), (6, 3, 0), (14, 3, 15)],
        5: [(6, 3, 1), (1, 2, 2)],
    }


def test_extract_tuple():
    assert extract_tuple("3 blue, 4 red") == (4, 0, 3)
    assert extract_tuple("1 red, 2 green, 6 blue") == (1, 2, 6)
    assert extract_tuple("2 green") == (0, 2, 0)


def test_part_1(example_data):
    assert part_1(example_data) == 8


def test_part_2(example_data):
    assert part_2(example_data) == 2286
