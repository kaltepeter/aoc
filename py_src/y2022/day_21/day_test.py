import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert (example_data) == {
        "root": "pppw + sjmn",
        "dbpl": 5,
        "cczh": "sllz + lgvd",
        "zczc": 2,
        "ptdq": "humn - dvpt",
        "dvpt": 3,
        "lfqf": 4,
        "humn": 5,
        "ljgn": 2,
        "sjmn": "drzm * dbpl",
        "sllz": 4,
        "pppw": "cczh / lfqf",
        "lgvd": "ljgn * ptdq",
        "drzm": "hmdt - zczc",
        "hmdt": 32,
    }


def test_part_1(example_data):
    assert part_1(example_data) == 152


def test_part_2(example_data):
    assert part_2(example_data) == 301
