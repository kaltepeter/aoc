import os
from pathlib import Path

from .day import process_input, part_1, part_2, check_unique


base_path = Path(__file__).parent


def test_check_unique():
    assert check_unique("abcd") == True
    assert check_unique("mjqj") == False


def test_process_input():
    assert process_input(os.path.join(base_path, "example.txt")) == [
        "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
        "bvwbjplbgvbhsrlpgdmjqwftvncz",
        "nppdvjthqldpwncqszvftbrmjlhg",
        "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
        "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
    ]


def test_part_1():
    signal_data = process_input(os.path.join(base_path, "example.txt"))
    assert part_1(signal_data[0]) == 7
    assert part_1(signal_data[1]) == 5
    assert part_1(signal_data[2]) == 6
    assert part_1(signal_data[3]) == 10
    assert part_1(signal_data[4]) == 11


def test_part_2():
    signal_data = process_input(os.path.join(base_path, "example.txt"))
    assert part_2(signal_data) == 0
