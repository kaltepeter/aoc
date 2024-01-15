import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert example_data == [
        ((19, 13, 30), (-2, 1, -2)),
        ((18, 19, 22), (-1, -1, -2)),
        ((20, 25, 34), (-2, -2, -4)),
        ((12, 31, 28), (-1, -2, -1)),
        ((20, 19, 15), (1, -5, -3)),
    ]


def test_part_1(example_data):
    assert part_1(example_data) == 2


def test_part_2(example_data):
    assert part_2(example_data) == 47
