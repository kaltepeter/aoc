import os
import pytest

from pathlib import Path
from .day import (
    are_ranges_overlapping,
    are_ranges_overlapping_at_all,
    process_input,
    part_1,
    part_2,
)

base_path = Path(__file__).parent


def test_are_ranges_overlapping():
    assert are_ranges_overlapping((2, 4), (6, 8)) == False  # less, less | more, more
    assert are_ranges_overlapping((2, 3), (4, 5)) == False  # less, less | more, more
    assert are_ranges_overlapping((5, 7), (7, 9)) == False  # less, less | more, more
    assert are_ranges_overlapping((2, 8), (3, 7)) == True  # less, more | more, less
    assert are_ranges_overlapping((6, 6), (4, 6)) == True  # more, equal | less, equal
    assert are_ranges_overlapping((2, 6), (4, 8)) == False  # less, less | more, more
    assert are_ranges_overlapping((12, 12), (12, 12)) == True  # eql, eql
    assert (
        are_ranges_overlapping((12, 15), (10, 13)) == False
    )  # more, more | less, less
    assert are_ranges_overlapping((18, 22), (12, 30)) == True  # more, less | less, more
    assert (
        are_ranges_overlapping((12, 18), (12, 13)) == True
    )  # equal, more | equal, less
    assert (
        are_ranges_overlapping((12, 20), (12, 16)) == True
    )  # equal, more | equal, less
    assert (
        are_ranges_overlapping((5, 12), (12, 12)) == True
    )  # less, equal | more, equal
    assert are_ranges_overlapping((5, 12), (5, 12)) == True

    with pytest.raises(ValueError):
        are_ranges_overlapping((3, 10), (3, 2))
        are_ranges_overlapping((10, 3), (2, 3))


def test_are_ranges_overlapping_at_all():
    assert (
        are_ranges_overlapping_at_all((2, 4), (6, 8)) == False
    )  # less, less | more, more
    assert (
        are_ranges_overlapping_at_all((2, 3), (4, 5)) == False
    )  # less, less | more, more
    assert (
        are_ranges_overlapping_at_all((5, 7), (7, 9)) == True
    )  # less, less | more, more
    assert (
        are_ranges_overlapping_at_all((2, 8), (3, 7)) == True
    )  # less, more | more, less
    assert (
        are_ranges_overlapping_at_all((6, 6), (4, 6)) == True
    )  # more, equal | less, equal
    assert (
        are_ranges_overlapping_at_all((2, 6), (4, 8)) == True
    )  # less, less | more, more


def test_process_input():
    assert process_input(os.path.join(base_path, "example.txt")) == [
        ((2, 4), (6, 8)),
        ((2, 3), (4, 5)),
        ((5, 7), (7, 9)),
        ((2, 8), (3, 7)),
        ((6, 6), (4, 6)),
        ((2, 6), (4, 8)),
    ]


def test_part_1():
    assert part_1(process_input(os.path.join(base_path, "example.txt"))) == 2


def test_part_2():
    assert part_2(process_input(os.path.join(base_path, "example.txt"))) == 4
