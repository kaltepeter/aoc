import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input, ranges_overlap

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_ranges_overlap():
    assert ranges_overlap((0, 3), [(0, 1)]) == True
    assert ranges_overlap((0, 3), [(1, 2)]) == True
    assert ranges_overlap((0, 3), [(2, 3)]) == True
    assert ranges_overlap((0, 3), [(3, 4)]) == True
    assert ranges_overlap((5, 8), [(3, 4)]) == False

    assert ranges_overlap((6, 9), [(0, 1)]) == False
    assert ranges_overlap((6, 9), [(5, 6)]) == True
    assert ranges_overlap((6, 9), [(6, 7)]) == True
    assert ranges_overlap((6, 9), [(7, 8)]) == True
    assert ranges_overlap((6, 9), [(8, 9)]) == True
    assert ranges_overlap((6, 9), [(9, 10)]) == True


def test_process_input(example_data):
    assert list(example_data)[0] == "467..114.."


def test_part_1(example_data):
    assert part_1(example_data) == 4361


def test_part_2(example_data):
    assert part_2(example_data) == 467835
