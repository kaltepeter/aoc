import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert example_data == (
        [79, 14, 55, 13],
        {
            "seed_to_soil": [(50, 98, 2), (52, 50, 48)],
            "soil_to_fertilizer": [(0, 15, 37), (37, 52, 2), (39, 0, 15)],
            "fertilizer_to_water": [(49, 53, 8), (0, 11, 42), (42, 0, 7), (57, 7, 4)],
            "water_to_light": [(88, 18, 7), (18, 25, 70)],
            "light_to_temperature": [(45, 77, 23), (81, 45, 19), (68, 64, 13)],
            "temperature_to_humidity": [(0, 69, 1), (1, 0, 69)],
            "humidity_to_location": [(60, 56, 37), (56, 93, 4)],
        },
    )


def test_part_1(example_data):
    assert part_1(example_data) == 35


def test_part_2(example_data):
    assert part_2(example_data) == 46
