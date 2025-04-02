import os
from pathlib import Path

import pytest
from .day import part_1, part_2, process_input

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


@pytest.fixture()
def example_data_2():
    return process_input(os.path.join(base_path, "example2.txt"))


def test_process_input(example_data):
    assert example_data == ({
        "0": [(8, 1), (5, 2), (7, 3), (4, 4)],
        "A": [(6, 5), (8, 8), (9, 9)]
    }, (12, 12))


# @pytest.mark.parametrize(
#         "pairs, expected",
#         [
#             (
#                 [(8, 1), (5, 2), (7, 3), (4, 4)], 
#                 [((8, 1), (7, 3)), ((5, 2), (4, 4))]
#             ),
#             (
#                 [(6, 5), (8, 8), (9, 9)], 
#                 [((8, 8), (9, 9))]
#             ),
#         ]
# )
# def test_find_aligned_pairs(pairs: List[Coord], expected: List[tuple[Coord, Coord]]):
#     assert find_aligned_pairs(pairs) == expected


def test_part_1(example_data):
    assert part_1(example_data) == 14
    

def test_part_2(example_data):
    assert part_2(example_data) == 34


def test_part_2_example_2(example_data_2):
    assert part_2(example_data_2) == 9