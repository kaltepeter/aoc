import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert example_data == {
        1: {
            "ore": (4, 0, 0),
            "clay": (2, 0, 0),
            "obsidian": (3, 14, 0),
            "geode": (2, 0, 7),
        },
        2: {
            "ore": (2, 0, 0),
            "clay": (3, 0, 0),
            "obsidian": (3, 8, 0),
            "geode": (3, 0, 12),
        },
    }


def test_part_1(example_data):
    assert part_1(example_data) == 33


def test_part_2(example_data):
    assert part_2(example_data) == 0
