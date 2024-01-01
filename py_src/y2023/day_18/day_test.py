import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input, convert_hex

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert next(example_data) == [
        ("R", 6.0, "#70c710"),
        ("D", 5.0, "#0dc571"),
        ("L", 2.0, "#5713f0"),
        ("D", 2.0, "#d2c081"),
        ("R", 2.0, "#59c680"),
        ("D", 2.0, "#411b91"),
        ("L", 5.0, "#8ceee2"),
        ("U", 2.0, "#caa173"),
        ("L", 1.0, "#1b58a2"),
        ("U", 2.0, "#caa171"),
        ("R", 2.0, "#7807d2"),
        ("U", 3.0, "#a77fa3"),
        ("L", 2.0, "#015232"),
        ("U", 2.0, "#7a21e3"),
    ]


def test_hex_codes(example_data):
    assert convert_hex(next(example_data)) == [
        ("R", 461937.0),
        ("D", 56407.0),
        ("R", 356671.0),
        ("D", 863240.0),
        ("R", 367720.0),
        ("D", 266681.0),
        ("L", 577262.0),
        ("U", 829975.0),
        ("L", 112010.0),
        ("D", 829975.0),
        ("L", 491645.0),
        ("U", 686074.0),
        ("L", 5411.0),
        ("U", 500254.0),
    ]


def test_part_1(example_data):
    assert part_1(next(example_data)) == 62


def test_part_2(example_data):
    assert part_2(next(example_data)) == 952408144115
