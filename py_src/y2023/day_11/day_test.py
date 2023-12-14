import os
from pathlib import Path

import pytest
from .day import (
    part_1,
    part_2,
    process_input,
    find_galaxies,
    expand_space,
    calculate_galaxy_positions,
)

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert example_data == [
        "...#......",
        ".......#..",
        "#.........",
        "..........",
        "......#...",
        ".#........",
        ".........#",
        "..........",
        ".......#..",
        "#...#.....",
    ]


def test_find_galaxies(example_data):
    assert find_galaxies(example_data)[0] == {
        (3, 0),
        (7, 1),
        (0, 2),
        (6, 4),
        (1, 5),
        (9, 6),
        (7, 8),
        (0, 9),
        (4, 9),
    }

    assert find_galaxies(example_data)[1] == ([2, 5, 8], [3, 7])


def test_expand_space(example_data):
    expanded_data = expand_space(
        example_data,
        (
            {
                (3, 0),
                (7, 1),
                (0, 2),
                (6, 4),
                (1, 5),
                (9, 6),
                (7, 8),
                (0, 9),
                (4, 9),
            },
            ([2, 5, 8], [3, 7]),
        ),
    )

    assert len(expanded_data) == 12
    assert len(expanded_data[0]) == 13


def test_calculate_new_galaxy_positions(example_data):
    expanded_data = expand_space(
        example_data,
        (
            {
                (3, 0),
                (7, 1),
                (0, 2),
                (6, 4),
                (1, 5),
                (9, 6),
                (7, 8),
                (0, 9),
                (4, 9),
            },
            ([2, 5, 8], [3, 7]),
        ),
    )

    new_galaxies = find_galaxies(expanded_data)

    assert new_galaxies[0] == {
        (4, 0),
        (9, 1),
        (0, 2),
        (8, 5),
        (1, 6),
        (12, 7),
        (9, 10),
        (0, 11),
        (5, 11),
    }

    assert new_galaxies[1] == ([2, 3, 6, 7, 10, 11], [3, 4, 8, 9])


def test_calculate_galaxy_positions(example_data):
    galaxy_list = find_galaxies(example_data)
    new_galaxies = calculate_galaxy_positions(galaxy_list)

    assert new_galaxies == 374


def test_part_1(example_data):
    assert part_1(example_data) == 374


def test_part_2(example_data):
    assert part_2(example_data, 10) == 1030
    assert part_2(example_data, 100) == 8410
