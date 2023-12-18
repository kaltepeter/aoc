import os
from pathlib import Path
from copy import deepcopy

import pytest
from .day import part_1, part_2, process_input, calculate_load, spin_cycle

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert next(example_data) == [
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


def test_spin_cycle(example_data):
    example = next(example_data)
    result = tuple(example)
    for _ in range(3):
        result = spin_cycle(result)

    assert result == tuple(
        [
            ".....#....",
            "....#...O#",
            ".....##...",
            "..O#......",
            ".....OOO#.",
            ".O#...O#.#",
            "....O#...O",
            ".......OOO",
            "#...O###.O",
            "#.OOO#...O",
        ]
    )


def test_part_1(example_data):
    assert part_1(next(example_data)) == 136


def test_part_2(example_data):
    assert part_2(next(example_data)) == 64
