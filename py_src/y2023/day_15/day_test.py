import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input, holiday_hash

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_holiday_hash():
    assert holiday_hash("HASH") == 52


def test_process_input(example_data):
    assert next(example_data) == [
        "rn=1",
        "cm-",
        "qp=3",
        "cm=2",
        "qp-",
        "pc=4",
        "ot=9",
        "ab=5",
        "pc-",
        "pc=6",
        "ot=7",
    ]


def test_part_1(example_data):
    assert part_1(next(example_data)) == 1320


def test_part_2(example_data):
    assert part_2(next(example_data)) == 145
