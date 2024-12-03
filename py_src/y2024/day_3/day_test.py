import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))

@pytest.fixture()
def example_data2():
    return process_input(os.path.join(base_path, "example2.txt"))

def test_process_input(example_data):
    assert example_data == "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))" 


def test_part_1(example_data):
    assert part_1(example_data) == 161 


def test_part_2(example_data2):
    assert part_2(example_data2) == 48 
