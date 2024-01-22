import os
from pathlib import Path

import pytest
from .day import (
    part_1,
    part_2,
    process_input,
    calculate_start_pipe,
    get_neighbor_coords,
    lookup_char,
    CharMap,
    count_inversions,
)

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert list(example_data)[0:2] == [
        [
            ".....",
            ".S-7.",
            ".|.|.",
            ".L-J.",
            ".....",
        ],
        [
            "..F7.",
            ".FJ|.",
            "SJ.L7",
            "|F--J",
            "LJ...",
        ],
    ]


def test_get_neighbor_coords():
    assert get_neighbor_coords((1, 1), (0, 4), (0, 4)) == [
        (0, 1),
        (2, 1),
        (1, 0),
        (1, 2),
    ]

    assert get_neighbor_coords((0, 2), (0, 4), (0, 4)) == [
        (1, 2),
        (0, 1),
        (0, 3),
    ]


def test_count_inversions(example_data):
    example = list(example_data)[0]
    assert count_inversions({(1, 1), (2, 1), (3, 1)}, example[1], 0, 1) == 0
    assert count_inversions({(1, 2), (3, 2)}, example[2], 0, 2) == 0
    assert count_inversions({(1, 2), (3, 2)}, example[2], 2, 2) == 1


def test_lookup_char():
    assert lookup_char((1, 1), (1, 2), (2, 1)) == CharMap.EFF


def test_calculate_start_pipe(example_data):
    data = list(example_data)
    assert calculate_start_pipe(data[0]) == [(1, 1), CharMap.EFF]
    assert calculate_start_pipe(data[1]) == [(0, 2), CharMap.EFF]


def test_part_1(example_data):
    examples = list(example_data)
    assert part_1(examples[0]) == 4
    assert part_1(examples[1]) == 8


def test_part_2(example_data):
    examples = list(example_data)
    assert part_2(examples[0]) == 1
    assert part_2(examples[1]) == 1
    assert part_2(examples[2]) == 4
    assert part_2(examples[3]) == 4
    assert part_2(examples[4]) == 8
    assert part_2(examples[5]) == 10  # edge case
