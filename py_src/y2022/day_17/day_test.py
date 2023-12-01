import os
from pathlib import Path

import pytest
from .day import (
    get_normalized_bit,
    get_set_bit_indexes,
    modify_bit_range,
    part_1,
    part_2,
    process_input,
)

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert next(example_data) == ">"
    assert next(example_data) == ">"
    assert len(list(example_data)) == 38


def test_get_normalized_bit():
    assert get_normalized_bit(0b0111000, 3) == True
    assert get_normalized_bit(0b0111000, 2) == False


def test_get_set_bit_indexes():
    assert get_set_bit_indexes(0b0111000) == [3, 4, 5]


def test_modify_bit_range():
    assert modify_bit_range(0b0111100, 3, 5, 1) == 0b1110100
    assert modify_bit_range(0b0111100, 2, 4, -1) == 0b0101110


def get_bit():
    assert get_bit(0b0111000, 3) == 1
    assert get_bit(0b0111000, 2) == 0


def test_part_1(example_data):
    assert part_1(example_data) == 3068


def skip_test_part_2(example_data):
    assert part_2(example_data) == 0
