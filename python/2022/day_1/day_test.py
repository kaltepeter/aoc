import os
from pathlib import Path

from .day import process_input, calc_calories, part_1, part_2

base_path = Path(__file__).parent


def test_process_input():
    assert process_input(os.path.join(base_path, "example.txt")) == [
        {"items": [1000, 2000, 3000]},
        {
            "items": [4000],
        },
        {"items": [5000, 6000]},
        {"items": [7000, 8000, 9000]},
        {"items": [10000]},
    ]


def test_calc_calories():
    assert calc_calories({"items": [1000, 2000, 3000]}) == 6000


def test_part_1():
    elves = process_input(os.path.join(base_path, "example.txt"))
    assert part_1(elves) == 24000


def test_part_2():
    elves = process_input(os.path.join(base_path, "example.txt"))
    assert part_2(elves) == 45000
