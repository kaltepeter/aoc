import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"), 7)


def test_process_input(example_data):
    grid, byte_list, max_size = example_data
    assert len(grid.nodes) == 49
    assert len(byte_list) == 25
    assert max_size == 7


def test_part_1(example_data):
    assert part_1(example_data, 12) == 22


def test_part_2(example_data):
    assert part_2(example_data) == (6, 1)
