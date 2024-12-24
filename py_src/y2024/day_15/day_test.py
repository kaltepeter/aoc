import os
from pathlib import Path

import pytest
from .day import LargeWarehouse, part_1, part_2, process_input, process_input_large_warehouse

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


@pytest.fixture()
def example_data2():
    return process_input(os.path.join(base_path, "example2.txt"))


@pytest.fixture()
def example_data_large_warehouse():
    return process_input_large_warehouse(os.path.join(base_path, "example3.txt"))

@pytest.fixture()
def example_data_large_warehouse_larger():
    return process_input_large_warehouse(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    warehouse, moves = example_data
    assert warehouse.width == 10
    assert warehouse.height == 10
    assert len(warehouse.walls) == 37
    assert len(warehouse.boxes) == 21
    assert len(moves) == 700
    assert "\n" not in moves 
    assert warehouse.get_gps((4, 1)) == 104


def test_process_input_large_warehouse(example_data_large_warehouse):
    warehouse, moves = example_data_large_warehouse
    assert warehouse.width == 14
    assert warehouse.height == 7 
    assert len(warehouse.walls) == 50
    assert len(warehouse.boxes) == 3
    assert len(moves) == 11
    assert "\n" not in moves 
    assert warehouse.get_gps((4, 1)) == 104


def test_part_1(example_data):
    assert part_1(example_data) == 10092 


def test_part_1_example2(example_data2):
    assert part_1(example_data2) == 2028


def test_part_2(example_data_large_warehouse):
    assert part_2(example_data_large_warehouse) == 618
    
def test_part_2_larger(example_data_large_warehouse_larger):
    assert part_2(example_data_large_warehouse_larger) == 9021
