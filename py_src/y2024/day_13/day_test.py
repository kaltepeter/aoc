import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert example_data == [
        ((8400, 5400), (94, 34), (22, 67)),
        ((12748, 12176), (26, 66), (67, 21)),
        ((7870, 6450), (17, 86), (84, 37)),
        ((18641, 10279), (69, 23), (27, 71))
    ]


def test_part_1(example_data):
    assert part_1(example_data) == 480


def test_part_2(example_data):
    assert part_2(example_data) == 875318608908
