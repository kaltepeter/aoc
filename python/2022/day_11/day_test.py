from functools import partial
import os
from pathlib import Path
from .day import add, get_fn, multiply, part_1, part_2, process_input, worry_less
from deepdiff import DeepDiff

base_path = Path(__file__).parent


def test_worry_less():
    assert worry_less(30) == 10
    assert worry_less(31) == 10


def test_get_fn():
    monkey_0_op = get_fn(("old", "*", "19"))
    monkey_1_op = get_fn(("old", "+", "6"))
    monkey_2_op = get_fn(("old", "*", "old"))
    assert monkey_0_op(a=79) == 1501
    assert monkey_1_op(a=54) == 60
    assert monkey_2_op(a=79, b=79) == 6241


def test_process_input():
    res = process_input(os.path.join(base_path, "example.txt"))
    assert len(res) == 4

    assert not DeepDiff(
        [
            {
                "id": 0,
                "starting_items": [79, 98],
                "operation": partial(multiply, a=None, b=19),
                "old_args": ("a",),
                "test": (23, 2, 3),
                "inspections": 0,
            },
            {
                "id": 1,
                "starting_items": [54, 65, 75, 74],
                "operation": partial(add, a=None, b=6),
                "old_args": ("a",),
                "test": (19, 2, 0),
                "inspections": 0,
            },
            {
                "id": 2,
                "starting_items": [79, 60, 97],
                "operation": partial(multiply, a=None, b=None),
                "old_args": (
                    "a",
                    "b",
                ),
                "test": (13, 1, 3),
                "inspections": 0,
            },
            {
                "id": 3,
                "starting_items": [74],
                "operation": partial(multiply, a=None, b=3),
                "old_args": ("a",),
                "test": (17, 0, 1),
                "inspections": 0,
            },
        ],
        res,
    )


def test_part_1():
    data = process_input(os.path.join(base_path, "example.txt"))
    assert part_1(data) == 10605


def test_part_2():
    data = process_input(os.path.join(base_path, "example.txt"))
    assert part_2(data) == 2713310158
