import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input, Direction, calculate_pw, get_ranges

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert example_data == (
        [
            "        ...#",
            "        .#..",
            "        #...",
            "        ....",
            "...#.......#",
            "........#...",
            "..#....#....",
            "..........#.",
            "        ...#....",
            "        .....#..",
            "        .#......",
            "        ......#.",
        ],
        [10, "R", 5, "L", 5, "R", 10, "L", 4, "R", 5, "L", 5],
    )


def test_calculate_pw():
    assert calculate_pw(6, 8, Direction.RIGHT) == 6032


def test_get_ranges(example_data):
    board, _ = example_data
    assert get_ranges(board) == {
        0: (8, 11),
        1: (8, 11),
        2: (8, 11),
        3: (8, 11),
        4: (0, 11),
        5: (0, 11),
        6: (0, 11),
        7: (0, 11),
        8: (8, 15),
        9: (8, 15),
        10: (8, 15),
        11: (8, 15),
    }


def test_part_1(example_data):
    assert part_1(example_data) == 6032


def test_part_2(example_data):
    assert part_2(example_data) == 0
