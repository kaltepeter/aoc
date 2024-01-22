import os
from pathlib import Path

import pytest
from .day import (
    part_1,
    part_2,
    process_input,
)

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert next(example_data) == [
        ".|...\\....",
        "|.-.\\.....",
        ".....|-...",
        "........|.",
        "..........",
        ".........\\",
        "..../.\\\\..",
        ".-.-/..|..",
        ".|....-|.\\",
        "..//.|....",
    ]


def test_part_1(example_data):
    assert part_1(next(example_data)) == 46


def test_part_2(example_data):
    assert part_2(next(example_data)) == 51
