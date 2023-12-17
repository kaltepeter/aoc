import os
from pathlib import Path

import pytest
from .day import (
    part_1,
    part_2,
    process_input,
    find_pairs,
    find_mirrored_rows,
    process_rows,
    rotate90,
)

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


@pytest.fixture()
def example2_data():
    return process_input(os.path.join(base_path, "example2.txt"))


def test_process_input(example_data):
    notes = list(example_data)
    assert len(notes) == 2

    assert notes[0] == [
        "#.##..##.",
        "..#.##.#.",
        "##......#",
        "##......#",
        "..#.##.#.",
        "..##..##.",
        "#.#.##.#.",
    ]


def test_find_pairs():
    assert find_pairs([1, 2]) == [(1, 2)]
    assert find_pairs([2, 3, 10, 11]) == [(2, 3), (10, 11)]
    assert find_pairs([0, 5, 8, 13]) == []
    assert find_pairs([2, 10, 3, 15]) == [(2, 3)]


def test_find_mirrored_rows(example_data, example2_data):
    examples = list(example_data)
    example2 = list(example2_data)
    assert find_mirrored_rows(examples[0], (2, 3)) == 0
    assert find_mirrored_rows(examples[1], (3, 4)) == 4

    assert find_mirrored_rows(example2[0], (2, 3)) == 0
    assert find_mirrored_rows(example2[0], (6, 7)) == 7
    assert find_mirrored_rows(example2[0], (10, 11)) == 0


def test_process_rows(example_data, example2_data):
    example = list(example_data)
    assert process_rows(example[0]) == 0
    assert process_rows(example[1]) == 4
    assert process_rows(list(example2_data)[0]) == 7


def test_process_cols(example_data, example2_data):
    example = list(example_data)
    m_e1 = rotate90(example[0])
    m_e2 = rotate90(example[1])

    example2 = list(example2_data)
    m_e3 = rotate90(example2[0])
    m_e4 = rotate90(example2[1])

    assert process_rows(m_e1) == 5
    assert process_rows(m_e2) == 0
    assert process_rows(m_e3) == 0
    assert process_rows(m_e4) == 6


def test_part_1(example_data):
    assert part_1(list(example_data)) == 405


def test_part_2(example_data):
    assert part_2(list(example_data)) == 400
