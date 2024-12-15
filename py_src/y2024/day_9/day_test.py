import os
from pathlib import Path

import pytest
from .day import calculate_checksum, part_1, part_2, process_input

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_calculate_checksum():
    assert calculate_checksum([0,0,9,9,8,1,1,1,8,8,8,2,7,7,7,3,3,3,6,4,4,6,5,5,5,5,6,6]) == 1928


def test_process_input(example_data):
    assert next(example_data) == "2333133121414131402"


def test_part_1(example_data):
    assert part_1(next(example_data)) == 1928 


def test_part_2(example_data):
    assert part_2(next(example_data)) == 2858 
