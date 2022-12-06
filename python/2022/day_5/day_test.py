from pathlib import Path

import os
from .day import get_indexes_in_string, get_top_of_stacks, part_1, part_2, process_input


base_path = Path(__file__).parent


def test_get_top_of_stacks():
    assert get_top_of_stacks({1: ["N", "Z"], 2: ["D", "C", "M"], 3: ["P"]}) == "NDP"


def test_get_indexes_in_string():
    assert get_indexes_in_string("[W] [W]     [N] [L] [V] [W] [C]", "W") == [1, 5, 25]


def test_process_input():
    assert process_input(os.path.join(base_path, "example.txt")) == (
        {1: ["N", "Z"], 2: ["D", "C", "M"], 3: ["P"]},
        [(1, 2, 1), (3, 1, 3), (2, 2, 1), (1, 1, 2)],
    )


def test_part_1():
    stacks, moves = process_input(os.path.join(base_path, "example.txt"))
    assert part_1(stacks, moves) == "CMZ"


def test_part_2():
    stacks, moves = process_input(os.path.join(base_path, "example.txt"))
    assert part_2(stacks, moves) == "MCD"
