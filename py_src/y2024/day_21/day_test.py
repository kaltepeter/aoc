import os
from pathlib import Path

import pytest
from .day import calc_complexity, find_paths, part_1, part_2, process_input, numeric_keypad, directional_keypad

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert example_data == [
        "029A", "980A", "179A", "456A", "379A"
    ]


@pytest.mark.parametrize(
        "code, sequence, expected",
        [
            ("029A", 68, (68 * 29)),
            ("980A", 60, (60 * 980)),
            ("179A", 68, (68 * 179)),
            ("456A", 64, (64 * 456)),
            ("379A", 64, (64 * 379)),
        ]
)
def test_calc_complexity(example_data, code: str, sequence: str, expected: int):
    assert calc_complexity(code, sequence) == expected


@pytest.mark.parametrize(
        "code, expected",
        [
            ('029A', ['<A^A>^^AvvvA', '<A^A^>^AvvvA', '<A^A^^>AvvvA'])
        ]
)
def test_find_paths_numeric(code, expected):
    assert sorted(find_paths(code, True)) == sorted(expected)


def test_part_1(example_data):
    assert part_1(example_data) == 126384


def test_part_2(example_data):
    assert part_2(example_data) == 154115708116294
