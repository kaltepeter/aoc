import os
from pathlib import Path

import numpy as np
import pytest
from .day import get_next_secret_number, get_x_secret_number, mix_number, part_1, part_2, process_input, prune_number

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert example_data == [
        1, 10, 100, 2024
    ]


def test_mix_number():
    assert mix_number(42, 15) == 37


def test_prune_number():
    assert prune_number(100000000) == 16113920


def test_get_next_secret_number():
        assert get_next_secret_number(123) == 15887950


@pytest.mark.parametrize(
          "secret_number, iterations, expected",
          [
               (123, 1, 15887950),
               (123, 2, 16495136), 
               (123, 9, 7753432 )
          ]
)
def test_get_x_secret_number(secret_number: int, iterations: int, expected: int):
     sn, _ = get_x_secret_number(secret_number, iterations)
     assert sn == expected


def test_part_1(example_data):
    assert part_1(example_data) == 37327623


def test_part_2():
    assert part_2([1, 2, 3, 2024]) == 23
