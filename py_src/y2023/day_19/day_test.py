import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input, calculate_ratings

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    expected_workflows = {
        "px": [("a<2006", "qkq"), ("m>2090", "A"), ("OUT", "rfg")],
        "pv": [("a>1716", "R"), ("OUT", "A")],
        "lnx": [("m>1548", "A"), ("OUT", "A")],
        "rfg": [("s<537", "gd"), ("x>2440", "R"), ("OUT", "A")],
        "qs": [("s>3448", "A"), ("OUT", "lnx")],
        "qkq": [("x<1416", "A"), ("OUT", "crn")],
        "crn": [("x>2662", "A"), ("OUT", "R")],
        "in": [("s<1351", "px"), ("OUT", "qqz")],
        "qqz": [("s>2770", "qs"), ("m<1801", "hdj"), ("OUT", "R")],
        "gd": [("a>3333", "R"), ("OUT", "R")],
        "hdj": [("m>838", "A"), ("OUT", "pv")],
    }

    expected_parts = [
        {"x": 787, "m": 2655, "a": 1222, "s": 2876},
        {"x": 1679, "m": 44, "a": 2067, "s": 496},
        {"x": 2036, "m": 264, "a": 79, "s": 2244},
        {"x": 2461, "m": 1339, "a": 466, "s": 291},
        {"x": 2127, "m": 1623, "a": 2188, "s": 1013},
    ]

    result = next(example_data)
    assert result[0] == expected_workflows
    assert result[1] == expected_parts


def test_calculate_ratings(example_data):
    accepted_parts = [
        {"x": 787, "m": 2655, "a": 1222, "s": 2876},
        {"x": 2036, "m": 264, "a": 79, "s": 2244},
        {"x": 2127, "m": 1623, "a": 2188, "s": 1013},
    ]
    assert (calculate_ratings(accepted_parts)) == 19114


def test_part_1(example_data):
    assert part_1(next(example_data)) == 19114


def test_part_2(example_data):
    assert part_2(next(example_data)) == 0
