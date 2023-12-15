import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input, find_broken_springs, unfold

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    data = list(example_data)
    map_1 = data[0]
    row_1 = map_1[0]

    assert len(map_1) == 6
    assert row_1[0] == "#.#.###"
    assert row_1[1] == [1, 1, 3]

    map_2 = data[1]
    row_2 = map_2[1]
    assert len(map_2) == 6
    assert row_2[0] == ".??..??...?##."
    assert row_2[1] == [1, 1, 3]


def test_find_broken_springs():
    assert (
        find_broken_springs(
            (
                "???.###",
                (1, 1, 3),
            )
        )
        == 1
    )
    assert (
        find_broken_springs(
            (
                ".??..??...?##.",
                (1, 1, 3),
            )
        )
        == 4
    )
    assert (
        find_broken_springs(
            (
                "?###????????",
                (3, 2, 1),
            )
        )
        == 10
    )


def test_unfold(example_data):
    assert unfold((".#", (1,))) == (
        ".#?.#?.#?.#?.#",
        (
            1,
            1,
            1,
            1,
            1,
        ),
    )

    example = list(example_data)[1]
    assert unfold((example[0][0], tuple(example[0][1]))) == (
        "???.###????.###????.###????.###????.###",
        (
            1,
            1,
            3,
            1,
            1,
            3,
            1,
            1,
            3,
            1,
            1,
            3,
            1,
            1,
            3,
        ),
    )


def test_part_1(example_data):
    example = list(example_data)[1]
    assert part_1(example) == 21


def test_part_2(example_data):
    example = list(example_data)[1]
    assert part_2(example) == 525152
