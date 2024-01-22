import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input, calculate_steps

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert example_data == [
        [0, 3, 6, 9, 12, 15],
        [1, 3, 6, 10, 15, 21],
        [10, 13, 16, 21, 30, 45],
    ]


def test_calculate_steps():
    assert calculate_steps([0, 3, 6, 9, 12, 15]) == [3, 3, 3, 3, 3]
    assert calculate_steps(
        [
            12,
            22,
            30,
            36,
            40,
            42,
            42,
            40,
            36,
            30,
            22,
            12,
            0,
            -14,
            -30,
            -48,
            -68,
            -90,
            -114,
            -140,
            -168,
        ]
    ) == [
        10,
        8,
        6,
        4,
        2,
        0,
        -2,
        -4,
        -6,
        -8,
        -10,
        -12,
        -14,
        -16,
        -18,
        -20,
        -22,
        -24,
        -26,
        -28,
    ]
    assert calculate_steps(
        [
            10,
            8,
            6,
            4,
            2,
            0,
            -2,
            -4,
            -6,
            -8,
            -10,
            -12,
            -14,
            -16,
            -18,
            -20,
            -22,
            -24,
            -26,
            -28,
        ]
    ) == [-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2]


def test_part_1(example_data):
    assert part_1(example_data) == 114


def test_part_2(example_data):
    assert part_2(example_data) == 2
