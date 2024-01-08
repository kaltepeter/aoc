import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input, Brick
import string

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_init(example_data):
    brick = example_data[0]
    assert (brick.name) == 0
    assert (brick.location) == [1, 0, 1, 1, 2, 1]


def test_repr(example_data):
    brick = example_data[0]
    assert (repr(brick)) == "[1, 0, 1, 1, 2, 1]"


@pytest.mark.parametrize(
    "b1,b2,expected",
    [
        (0, 1, True),
        (0, 2, True),
        (0, 3, False),
        (1, 2, False),
        (1, 3, True),
        (1, 4, True),
    ],
)
def test_overlaps(b1, b2, expected, request):
    example_data = request.getfixturevalue("example_data")
    brick1 = example_data[b1]
    brick2 = example_data[b2]
    assert brick1.overlaps(brick2) == expected


def test_process_input(example_data):
    assert len(example_data) == 7


def test_part_1(example_data):
    assert part_1(example_data) == 5


def test_part_2(example_data):
    assert part_2(example_data) == 7
