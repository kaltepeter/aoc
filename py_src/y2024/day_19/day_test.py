import os
from pathlib import Path
from typing import List

import pytest
from .day import compute_design_combos, part_1, part_2, process_input

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


@pytest.fixture()
def example_data2():
    return process_input(os.path.join(base_path, "example2.txt"))


def test_process_input(example_data):
    available_towels, towel_patterns = example_data
    assert available_towels == ["r", "wr", "b", "g", "bwu", "rb", "gb", "br"]
    assert len(towel_patterns) == 8


@pytest.mark.parametrize(
    "pattern, expected_count",
    [
        ("brwrr", 2),
        ('bggr', 1),
        ('gbbr', 4),
        ("rrbgbr", 6),
        ('bwurrg', 1),
        ('brgr', 2),
        ('ubwu', 0),
        ('bbrgwb', 0)
    ])
def test_compute_design_combos(example_data, pattern: str, expected_count: int):
    available_towels = example_data[0]
    assert compute_design_combos(pattern, available_towels) == expected_count


def test_part_1_example2(example_data2):
    assert part_1(example_data2) == 0


def test_part_1(example_data):
    assert part_1(example_data) == 6 


def test_part_2(example_data):
    assert part_2(example_data) == 16 
