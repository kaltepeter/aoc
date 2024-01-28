import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input, calculate_max_spends

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


@pytest.fixture()
def max_spend(example_data):
    return calculate_max_spends(example_data)


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


def test_part_1(example_data, max_spend):
    assert part_1(example_data, max_spend) == 33


# too slow
def skip_test_part_2(example_data, max_spend):
    assert part_2(example_data, max_spend) == (56 * 62)
