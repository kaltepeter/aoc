import os
from pathlib import Path

from .day import get_signal_strength, part_1, part_2, process_input

base_path = Path(__file__).parent


def test_get_signal_strength():
    vals = {
        0: 1,
        1: 1,
        2: 1,
        19: 21,
        59: 19,
        99: 18,
        139: 21,
        179: 16,
        219: 18,
    }
    assert get_signal_strength(vals) == 13140


def test_process_input():
    assert process_input(os.path.join(base_path, "example.txt"))[:3] == [
        ("addx", 15),
        ("addx", -11),
        ("addx", 6),
    ]


def test_part_1():
    data = process_input(os.path.join(base_path, "example.txt"))
    assert (
        part_1(
            [
                ("noop", 0),
                ("addx", 3),
                ("addx", -5),
            ]
        )
        == -720
    )
    assert part_1(data) == 13140


def test_part_2():
    data = process_input(os.path.join(base_path, "example.txt"))
    assert (
        part_2(data)
        == "##..##..##..##..##..##..##..##..##..##..\n###...###...###...###...###...###...###.\n####....####....####....####....####....\n#####.....#####.....#####.....#####.....\n######......######......######......####\n#######.......#######.......#######....."
    )
