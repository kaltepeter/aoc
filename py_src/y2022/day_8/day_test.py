import os
from pathlib import Path

from .day import (
    get_indexes_to_check,
    get_scenic_score,
    is_visible,
    process_input,
    part_1,
    part_2,
)


base_path = Path(__file__).parent


def test_get_indexes_to_check():
    assert get_indexes_to_check(5, 5, (1, 1)) == {
        (0, 1),
        (2, 1),
        (3, 1),
        (4, 1),
        (1, 0),
        (1, 2),
        (1, 3),
        (1, 4),
    }

    assert get_indexes_to_check(5, 5, (0, 2)) == {
        (0, 0),
        (0, 1),
        (0, 3),
        (0, 4),
        (1, 2),
        (2, 2),
        (3, 2),
        (4, 2),
    }


def test_is_visible():
    assert is_visible([2, 5, 5, 1, 2], 2) == True
    assert is_visible([2, 5, 5, 1, 2], 1) == True
    assert is_visible([2, 5, 5, 1, 2], 3) == False
    assert is_visible([2, 5, 5, 1, 2], 4) == True
    assert is_visible([2, 5, 5, 1, 2], 0) == True
    assert is_visible([3, 5, 3, 5, 3], 1) == True
    assert is_visible([3, 5, 3, 5, 3], 2) == False
    assert is_visible([3, 3, 5, 4, 9], 3) == False
    assert is_visible([7, 1, 3, 4, 9], 3) == False


def test_get_scenic_score():
    assert get_scenic_score([2, 5, 5, 1, 2], 2) == (1, 2)
    assert get_scenic_score([3, 5, 3, 5, 3], 1) == (1, 2)
    assert get_scenic_score([3, 3, 5, 4, 9], 2) == (2, 2)
    assert get_scenic_score([3, 5, 3, 5, 3], 3) == (2, 1)


def test_process_input():
    assert process_input(os.path.join(base_path, "example.txt")) == [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0],
    ]


def test_part_1():
    data = process_input(os.path.join(base_path, "example.txt"))
    assert part_1(data) == 21


def test_part_2():
    data = process_input(os.path.join(base_path, "example.txt"))
    assert part_2(data) == 8
