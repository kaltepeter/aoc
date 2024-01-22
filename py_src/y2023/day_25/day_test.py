import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert example_data["jqt"] == {"rhn", "xhk", "nvd", "ntq"}
    assert example_data["hfx"] == {"xhk", "rhn", "bvb", "pzl", "ntq"}


def test_part_1(example_data):
    assert part_1(example_data) == 54


def test_part_2(example_data):
    assert part_2(example_data) == 0
