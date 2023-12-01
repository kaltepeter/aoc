import os
from pathlib import Path

import pytest
from .day import (
    part_1,
    part_2,
    process_input,
    replace_words_with_numbers,
    get_calibration_digits,
)

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


@pytest.fixture()
def example_data2():
    return process_input(os.path.join(base_path, "example2.txt"))


def test_process_input(example_data):
    assert list(example_data) == ["1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet"]


def test_get_calibration_digits(example_data):
    assert get_calibration_digits(list(example_data)) == [12, 38, 15, 77]
    assert get_calibration_digits(["hvkv8"]) == [88]


def test_replace_words_with_numbers(example_data):
    assert replace_words_with_numbers("oneblahtwo") == "1blah2"
    assert replace_words_with_numbers("eightwothree") == "8wo3"
    assert replace_words_with_numbers("hvkv8") == "hvkv8"
    assert replace_words_with_numbers("fourrhhhdmzcbvbldqlmb4") == "4rhhhdmzcbvbldqlmb4"


def test_part_1(example_data):
    assert part_1(example_data) == 142


def test_part_2(example_data2):
    # assert part_2(example_data) == 142
    assert part_2(example_data2) == 281
