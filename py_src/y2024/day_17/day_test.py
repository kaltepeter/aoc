import os
from pathlib import Path
from typing import List
import pytest
from .day import bst, bxc, bxl, find_specific_items, get_combo_operand, out, part_1, part_2, process_input, dv, run_program

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


@pytest.fixture()
def example_data2():
    return process_input(os.path.join(base_path, "example2.txt"))


@pytest.mark.parametrize(
        "op, expected", 
        [
            (2, 4), (5, 0)
        ]
        )
def test_adv(op, expected):
    registers = [16, 5, 6]
    assert dv(registers, op) == expected


@pytest.mark.parametrize(
        "op, expected",
        [
            (4, 1)
        ]
)
def test_bxl(op, expected):
    registers = [16, 5, 6]
    assert bxl(registers, op) == expected


def test_bst():
    registers = [16, 3, 20]
    assert bst(registers, 6) == 4


def test_bxc():
    assert bxc([16, 3, 20], 6) == 23


def test_out():
    assert out([16, 3, 20], 2) == 2


@pytest.mark.parametrize(
    "op, expected",
    [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 16),
        (5, 3),
        (6, 20),
    ],
)
def test_get_combo_operand(op, expected):
    registers = [16, 3, 20]
    assert get_combo_operand(registers, op) == expected


def test_get_combo_operand_throws_error():
    with pytest.raises(ValueError):
        assert get_combo_operand([1, 2, 3], 7)


def test_process_input(example_data):
    registers, program = example_data
    assert registers == [729, 0, 0]
    assert program == [0, 1, 5, 4, 3, 0]


@pytest.mark.parametrize(
    "register, program, expected",
    [
        ([0, 0, 9], [2, 6], ([0, 1, 9], [])),
        ([10, 0, 0], [5, 0, 5, 1, 5, 4], ([10, 0, 0], [0, 1, 2])),
        ([2024, 0, 0], [0,1,5,4,3,0], ([0, 0, 0], [4,2,5,6,7,7,7,7,3,1,0])),
        ([0, 29, 0], [1, 7], ([0, 26, 0], [])),
        ([0, 2024, 43690], [4, 0], ([0, 44354, 43690], []))
    ]
)
def test_run_program(register, program, expected):
    assert run_program(register, program) == expected


def test_part_1(example_data):
    assert part_1(example_data) == "4,6,3,5,6,3,5,2,1,0"


def test_part_2(example_data2):
    assert find_specific_items(example_data2, 2024, example_data2[1]) == 117440
    # assert part_2(example_data2) == 117440
