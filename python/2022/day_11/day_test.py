import os
from pathlib import Path
from .day import get_fn, part_1, process_input, worry_less

base_path = Path(__file__).parent


def test_worry_less():
    assert worry_less(30) == 10
    assert worry_less(31) == 10


def test_get_fn():
    assert get_fn(79, ("old", "*", "19")) == 1501
    assert get_fn(54, ("old", "+", "6")) == 60
    assert get_fn(79, ("old", "*", "old")) == 6241


def test_process_input():
    assert process_input(os.path.join(base_path, "example.txt")) == [
        {
            "id": 0,
            "starting_items": [79, 98],
            "operation": ("old", "*", "19"),
            "test": (23, 2, 3),
            "inspections": 0,
        },
        {
            "id": 1,
            "starting_items": [54, 65, 75, 74],
            "operation": ("old", "+", "6"),
            "test": (19, 2, 0),
            "inspections": 0,
        },
        {
            "id": 2,
            "starting_items": [79, 60, 97],
            "operation": ("old", "*", "old"),
            "test": (13, 1, 3),
            "inspections": 0,
        },
        {
            "id": 3,
            "starting_items": [74],
            "operation": ("old", "+", "3"),
            "test": (17, 0, 1),
            "inspections": 0,
        },
    ]


def test_part_1():
    data = process_input(os.path.join(base_path, "example.txt"))
    assert part_1(data) == 10605
