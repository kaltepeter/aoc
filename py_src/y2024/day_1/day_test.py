import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert example_data == ([1, 2, 3, 3, 3, 4], [3, 3, 3, 4, 5, 9])


def test_part_1(example_data):
    assert part_1(example_data) == 11


def test_part_2(example_data):
    assert part_2(example_data) == 31
