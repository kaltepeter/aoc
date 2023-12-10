import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input, run_path

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


@pytest.fixture()
def example_data_2():
    return process_input(os.path.join(base_path, "example2.txt"))


@pytest.fixture()
def example_data_3():
    return process_input(os.path.join(base_path, "example3.txt"))


def test_process_input(example_data):
    assert example_data[0] == "RL"
    assert example_data[1] == {
        "AAA": ("BBB", "CCC"),
        "BBB": ("DDD", "EEE"),
        "CCC": ("ZZZ", "GGG"),
        "DDD": ("DDD", "DDD"),
        "EEE": ("EEE", "EEE"),
        "GGG": ("GGG", "GGG"),
        "ZZZ": ("ZZZ", "ZZZ"),
    }


def test_process_input(example_data_2):
    assert example_data_2[0] == "LLR"
    assert example_data_2[1] == {
        "AAA": ("BBB", "BBB"),
        "BBB": ("AAA", "ZZZ"),
        "ZZZ": ("ZZZ", "ZZZ"),
    }


def test_run_path(example_data, example_data_2):
    assert run_path(*example_data) == 2
    assert run_path(*example_data_2) == 6


def test_run_path_for_ghosts(example_data_3):
    assert run_path(*example_data_3, "11A", True) == 2
    assert run_path(*example_data_3, "22A", True) == 3


def test_part_1(example_data):
    assert part_1(example_data) == 2


def test_part_2(example_data_3):
    assert part_2(example_data_3) == 6
