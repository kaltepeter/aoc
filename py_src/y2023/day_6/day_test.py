import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input, process_input_part_2

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


@pytest.fixture()
def example_data_2():
    return process_input_part_2(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert example_data == [(7, 9), (15, 40), (30, 200)]


def test_process_input_part_2(example_data_2):
    assert example_data_2 == (71530, 940200)


def test_part_1(example_data):
    assert part_1(example_data) == 288


def test_part_2(example_data_2):
    assert part_2(example_data_2) == 71503
