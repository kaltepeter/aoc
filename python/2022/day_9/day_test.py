import os
from pathlib import Path

import pytest

from .day import is_touching, move, process_input, part_1, part_2


base_path = Path(__file__).parent


def test_move():
    assert move((0, 0), ("R", 4)) == (4, 0)
    assert move((4, 0), ("U", 4)) == (4, -4)
    assert move((4, -4), ("L", 4)) == (0, -4)
    assert move((0, -4), ("D", 1)) == (0, -3)
    assert move((0, -3), ("R", 4)) == (4, -3)


def test_is_touching():
    assert is_touching((0, 0), (0, 0)) == True
    assert is_touching((0, 1), (0, 0)) == True
    assert is_touching((0, 2), (0, 0)) == False
    assert is_touching((1, 0), (0, 0)) == True
    assert is_touching((2, 0), (0, 0)) == False
    assert is_touching((1, 1), (0, 0)) == True
    assert is_touching((-1, -1), (0, 0)) == True
    assert is_touching((1, -1), (0, 0)) == True
    assert is_touching((-1, 1), (0, 0)) == True
    assert is_touching((3, 3), (2, 2)) == True
    assert is_touching((4, -1), (3, 0)) == True


def test_process_input():
    assert process_input(os.path.join(base_path, "example.txt")) == [
        ("R", 4),
        ("U", 4),
        ("L", 3),
        ("D", 1),
        ("R", 4),
        ("D", 1),
        ("L", 5),
        ("R", 2),
    ]


def test_part_1():
    data = process_input(os.path.join(base_path, "example.txt"))
    assert part_1(data) == 13


def test_part_2():
    data = process_input(os.path.join(base_path, "example.txt"))
    assert part_2(data) == 0
