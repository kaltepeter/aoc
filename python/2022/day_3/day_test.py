import os
import pytest
from pathlib import Path

from .day import (
    calc_priority,
    find_common_items,
    part_1,
    part_2,
    process_input,
    split_word_in_half,
)


base_path = Path(__file__).parent


def test_split_word_in_half():
    with pytest.raises(ValueError):
        split_word_in_half("abc")
    assert split_word_in_half("abcd") == ("ab", "cd")


def test_find_common_items():
    assert find_common_items(("abc", "ade")) == {"a"}
    assert find_common_items(("abc", "def")) == set()
    assert find_common_items(("abcc", "ccdef")) == {"c"}


def test_calc_priority():
    assert calc_priority("p") == 16
    assert calc_priority("L") == 38
    assert calc_priority("P") == 42
    assert calc_priority("v") == 22
    assert calc_priority("t") == 20
    assert calc_priority("s") == 19


def test_process_input():
    assert process_input(os.path.join(base_path, "example.txt")) == [
        {
            "compartment_1": "vJrwpWtwJgWr",
            "compartment_2": "hcsFMMfFFhFp",
            "common_items": {"p"},
        },
        {
            "compartment_1": "jqHRNqRjqzjGDLGL",
            "compartment_2": "rsFMfFZSrLrFZsSL",
            "common_items": {"L"},
        },
        {
            "compartment_1": "PmmdzqPrV",
            "compartment_2": "vPwwTWBwg",
            "common_items": {"P"},
        },
        {
            "compartment_1": "wMqvLMZHhHMvwLH",
            "compartment_2": "jbvcjnnSBnvTQFn",
            "common_items": {"v"},
        },
        {
            "compartment_1": "ttgJtRGJ",
            "compartment_2": "QctTZtZT",
            "common_items": {"t"},
        },
        {
            "compartment_1": "CrZsJsPPZsGz",
            "compartment_2": "wwsLwLmpwMDw",
            "common_items": {"s"},
        },
    ]


def test_part_1():
    assert part_1(process_input(os.path.join(base_path, "example.txt"))) == 157


def test_part_2():
    assert part_2(process_input(os.path.join(base_path, "example.txt"))) == 0
