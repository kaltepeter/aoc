import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert example_data == (
        (5, 5),
        [
            "...........",
            ".....###.#.",
            ".###.##..#.",
            "..#.#...#..",
            "....#.#....",
            ".##..S####.",
            ".##..#...#.",
            ".......##..",
            ".##.#.####.",
            ".##..##.##.",
            "...........",
        ],
    )


def test_part_1(example_data):
    assert part_1(example_data, 6) == 16


# Not relevant
# def test_part_2(example_data):
#     assert part_2(example_data, 6) == 16
#     assert part_2(example_data, 10) == 50
#     assert part_2(example_data, 50) == 1594
#     assert part_2(example_data, 100) == 6536
#     assert part_2(example_data, 500) == 167004
#     assert part_2(example_data, 1000) == 668697
#     assert part_2(example_data, 5000) == 16733044
