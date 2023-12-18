import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input, calculate_load

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert list(example_data)[0] == [
        "O....#....",
        "O.OO#....#",
        ".....##...",
        "OO.#O....O",
        ".O.....O#.",
        "O.#..O.#.#",
        "..O..#O..O",
        ".......O..",
        "#....###..",
        "#OO..#....",
    ]


def test_calculate_load():
    assert (
        calculate_load(
            [
                "OOOO.#.O..",
                "OO..#....#",
                "OO..O##..O",
                "O..#.OO...",
                "........#.",
                "..#....#.#",
                "..O..#.O.O",
                "..O.......",
                "#....###..",
                "#....#....",
            ]
        )
        == 136
    )


def test_part_1(example_data):
    assert part_1(list(example_data)[0]) == 136


def test_part_2(example_data):
    assert part_2(list(example_data)[0]) == 0
