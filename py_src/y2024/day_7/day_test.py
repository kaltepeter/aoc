import os
from pathlib import Path
from typing import List

import pytest
from .day import evaluate_expression, part_1, part_2, process_input

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))

@pytest.mark.parametrize(
        'nums, ops, expected',
        [
            ([10, 19], ('+',), 29),
            ([10, 19], ('*',), 190),
        ]
)
def test_evaluate_expression(nums: List[int], ops: List[str], expected: int):
    assert evaluate_expression(nums, ops) == expected


def test_process_input(example_data):
    assert len(example_data) == 9
    assert example_data[0] == (190, [10, 19])


def test_part_1(example_data):
    assert part_1(example_data) == 3749


def test_part_2(example_data):
    assert part_2(example_data) == 11387
