import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input, split_number

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert example_data == [125, 17]


@pytest.mark.parametrize(
        'blinks, expected',
        [
            (6, 22), 
            (25, 55312)
        ]
)
def test_part_1(example_data, blinks, expected):
    assert part_1(example_data, blinks) == expected


@pytest.mark.parametrize(
        'num_str, expected',
        [
            ('10', (1, 0)),
            ("1234", (12, 34)),
            ("123456", (123, 456)),
            ("12345678", (1234, 5678)),
            ("1000", (10, 0)),
        ]
)
def test_slit_number(num_str, expected):
    assert split_number(num_str) == expected


def test_part_2(example_data):
    assert part_2(example_data, 35) == 3604697
