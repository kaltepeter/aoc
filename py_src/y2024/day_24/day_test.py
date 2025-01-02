import os
from pathlib import Path

import pytest
from .day import (
    calculate_letter_values,
    is_list_valid,
    part_1,
    part_2,
    process_input,
    WireMap,
)

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


@pytest.fixture()
def example_data_small():
    return process_input(os.path.join(base_path, "example_small.txt"))


@pytest.fixture()
def example_data_swapped():
    return process_input(os.path.join(base_path, "example_swapped.txt"))


def test_process_input(example_data_small):
    wire_map, rule_map = example_data_small
    assert len(wire_map) == 6
    assert wire_map["y01"] == 1
    assert rule_map == {
        ("x00", "y00"): [("AND", "z00")],
        ("x01", "y01"): [("XOR", "z01")],
        ("x02", "y02"): [("OR", "z02")],
    }


def test_calculate_letter_values():
    wire_map = {
        "bfw": 1,
        "bqk": 1,
        "djm": 1,
        "ffh": 0,
        "fgs": 1,
        "frj": 1,
        "fst": 1,
        "gnj": 1,
        "hwm": 1,
        "kjc": 0,
        "kpj": 1,
        "kwq": 0,
        "mjb": 1,
        "nrd": 1,
        "ntg": 0,
        "pbm": 1,
        "psh": 1,
        "qhw": 1,
        "rvg": 0,
        "tgd": 0,
        "tnw": 1,
        "vdt": 1,
        "wpb": 0,
        "z00": 0,
        "z01": 0,
        "z02": 0,
        "z03": 1,
        "z04": 0,
        "z05": 1,
        "z06": 1,
        "z07": 1,
        "z08": 1,
        "z09": 1,
        "z10": 1,
        "z11": 0,
        "z12": 0,
    }
    assert calculate_letter_values(wire_map, "z") == 2024


@pytest.mark.parametrize(
    "wire_map, expected_result",
    [
        ({}, True),
        (
            {
                "x00": 1,
                "x01": 1,
                "x02": 0,
                "x03": 1,
                "y00": 1,
                "y01": 0,
                "y02": 1,
                "y03": 1,
                "z00": 0,
                "z01": 0,
                "z02": 0,
                "z03": 1,
                "z04": 1,
            },
            True,
        ),
        (
            {
                "x00": 1,
                "x01": 1,
                "x02": 0,
                "x03": 0,
                "y00": 1,
                "y01": 0,
                "y02": 1,
                "y03": 1,
                "z00": 0,
                "z01": 0,
                "z02": 0,
                "z03": 1,
                "z04": 1,
            },
            False,
        ),
    ],
)
def test_is_list_valid(wire_map: WireMap, expected_result: bool):
    assert is_list_valid(wire_map) == expected_result


def test_part_1(example_data):
    assert part_1(example_data) == 2024


@pytest.mark.skip('bad example')
def test_part_2(example_data):
    assert part_2(example_data) == "aaa,aoc,bbb,ccc,eee,ooo,z24,z99"
