import os
from pathlib import Path

import pytest
from .day import get_quadrant, part_1, part_2, process_input

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert len(example_data) == 12
    assert example_data[0] == ((0, 4), (3, -3))
    assert example_data[11] == ((9,5), (-3, -3))


@pytest.mark.parametrize(
        "coord, expected_quadrant",
        [
            ((49, 50), 1),
            ((51, 50), 2),
            ((50, 51), 0),
            ((49, 51), 0),
            ((49, 52), 3),
            ((51, 52), 4)
        ],
)
def test_get_quadrant(coord, expected_quadrant):
    assert get_quadrant(coord, 101, 103) == expected_quadrant


def test_part_1(example_data):
    assert part_1(example_data) == 21


def test_part_2(example_data):
    assert part_2(example_data) > 0
