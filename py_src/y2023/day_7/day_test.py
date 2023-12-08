import os
from pathlib import Path

import pytest
from functools import cmp_to_key
from .day import (
    part_1,
    part_2,
    process_input,
    compare_hands,
    calculate_total,
    sort_hands,
)

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert example_data == [
        ("32T3K", 765),
        ("T55J5", 684),
        ("KK677", 28),
        ("KTJJT", 220),
        ("QQQJA", 483),
    ]


def test_sort_hands(example_data):
    assert sort_hands(
        {
            0: [],
            1: [("32T3K", 765)],
            2: [("KK677", 28), ("KTJJT", 220)],
            4: [("T55J5", 684), ("QQQJA", 483)],
            5: [],
            8: [],
            16: [],
        }
    ) == [
        ("32T3K", 765),
        ("KTJJT", 220),
        ("KK677", 28),
        ("T55J5", 684),
        ("QQQJA", 483),
    ]


def test_calculate_total():
    ranked_hands = [
        ("32T3K", 765),
        ("KTJJT", 220),
        ("KK677", 28),
        ("T55J5", 684),
        ("QQQJA", 483),
    ]
    assert calculate_total(ranked_hands) == 6440


def test_compare_hands():
    assert compare_hands(("AAAAA", 10), ("AAAAA", 30)) == 0
    assert compare_hands(("KK677", 10), ("KTJJT", 30)) == 1
    assert compare_hands(("KTJJT", 10), ("KK677", 30)) == -1

    assert compare_hands(("T55J5", 10), ("QQQJA", 5)) == -1
    assert compare_hands(("QQQJA", 2), ("T55J5", 5)) == 1
    sorted_list = sorted([("KK677", 234), ("KTJJT", 50)], key=cmp_to_key(compare_hands))
    assert sorted_list == [("KTJJT", 50), ("KK677", 234)]

    sorted_list = sorted([("T55J5", 30), ("QQQJA", 5)], key=cmp_to_key(compare_hands))
    assert sorted_list == [("T55J5", 30), ("QQQJA", 5)]


def test_part_1(example_data):
    assert part_1(example_data) == 6440


def test_part_2(example_data):
    assert part_2(example_data) == 0
