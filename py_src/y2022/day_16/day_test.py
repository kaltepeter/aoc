import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert example_data.edges["AA"] == ["DD", "II", "BB"]
    assert example_data.edges["BB"] == ["CC", "AA"]
    assert example_data.edges["CC"] == ["DD", "BB"]
    assert len(example_data.edges.keys()) == 10

    assert "AA" not in example_data.flows
    assert example_data.flows["BB"] == 13
    assert example_data.flows["CC"] == 2


def test_part_1(example_data):
    assert part_1(example_data) == 1651


def test_part_2(example_data):
    assert part_2(example_data) == 1707
