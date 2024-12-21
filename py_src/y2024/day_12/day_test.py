import os
from pathlib import Path

import pytest
from .day import get_corner_count, part_1, part_2, process_input

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert example_data.number_of_nodes() == 100

@pytest.mark.parametrize(
        'region, expected',
        [
            ([(4, 4), (0, 7), (5, 5), (3, 4), (6, 5), (5, 4), (1, 8), (0, 6), (1, 7), (3, 3), (2, 6), (1, 6), (2, 5), (3, 5)], 22),
            ([(4, 7)], 4),
            ([(9, 5), (8, 4), (9, 4)], 6)
        ]
)
def test_get_corner_count(region, expected):
    assert get_corner_count(region) == expected


def test_part_1(example_data):
    assert part_1(example_data) == 1930 


def test_part_2(example_data):
    assert part_2(example_data) == 1206
