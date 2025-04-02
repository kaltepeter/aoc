import os
from pathlib import Path
from typing import List

import pytest
from .day import check_lock, part_1, part_2, process_input

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    locks, keys, height = example_data
    assert height == 6
    assert len(locks) == 2
    assert len(keys) == 3
    assert locks[0] == [0, 5, 3, 4, 3]
    assert locks[1] == [1, 2, 0, 5, 3]
    assert keys[0] == [5, 0, 2, 1, 3]
    assert keys[1] == [4, 3, 4, 0, 2]
    assert keys[2] == [3, 0, 2, 0, 1]


@pytest.mark.parametrize(
    "lock, key, height, expected",
    [
        ([0, 5, 3, 4, 3], [5, 0, 2, 1, 3], 6, False),
        ([0, 5, 3, 4, 3], [4, 3, 4, 0, 2], 6, False),
        ([0, 5, 3, 4, 3], [3, 0, 2, 0, 1], 6, True),
        ([1, 2, 0, 5, 3], [5, 0, 2, 1, 3], 6, False),
        ([1, 2, 0, 5, 3], [4, 3, 4, 0, 2], 6, True),
        ([1, 2, 0, 5, 3], [3, 0, 2, 0, 1], 6, True),
    ],
)
def test_check_lock(lock: List[int], key: List[int], height: int, expected: bool):
    assert check_lock(lock, key, height) == expected


def test_part_1(example_data):
    assert part_1(example_data) == 3


def test_part_2(example_data):
    assert part_2(example_data) == 0
