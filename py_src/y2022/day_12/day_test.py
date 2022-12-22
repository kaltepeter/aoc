import os
from pathlib import Path

from .day import part_1, process_input

# from .day import process_input

# from .day import part_1, process_input


base_path = Path(__file__).parent


def test_process_input():
    res = process_input(os.path.join(base_path, "example.txt"))
    assert res == []


def test_part_1():
    data = process_input(os.path.join(base_path, "example.txt"))
    assert part_1(data) == 31
