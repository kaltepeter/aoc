import os
from pathlib import Path
from .day import compare_ints, compare_pairs, part_1, part_2, process_input

base_path = Path(__file__).parent


def test_process_input():
    packets = process_input(os.path.join(base_path, "example.txt"))
    assert list(packets) == [
        [[1, 1, 3, 1, 1], [1, 1, 5, 1, 1]],
        [[[1], [2, 3, 4]], [[1], 4]],
        [[9], [[8, 7, 6]]],
        [[[4, 4], 4, 4], [[4, 4], 4, 4, 4]],
        [[7, 7, 7, 7], [7, 7, 7]],
        [[], [3]],
        [[[[]]], [[]]],
        [[1, [2, [3, [4, [5, 6, 7]]]], 8, 9], [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]],
    ]


def test_compare_ints():
    assert compare_ints(0, 2) == True
    assert compare_ints(2, 2) == True
    assert compare_ints(3, 2) == False


def test_compare_pairs():
    assert compare_pairs([1, 1, 3, 1, 1], [1, 1, 5, 1, 1], list()) == (
        [
            True,
            True,
            True,
            True,
            True,
        ],
        [],
        [],
    )
    assert compare_pairs([[1], [2, 3, 4]], [[1], 4], list()) == (
        [True, True],
        [],
        [],
    )
    assert compare_pairs([9], [[8, 7, 6]], list()) == ([False], [], [])

    assert compare_pairs([[4, 4], 4, 4], [[4, 4], 4, 4, 4], list()) == (
        [
            True,
            True,
            True,
            True,
        ],
        [],
        [4],
    )

    assert compare_pairs([7, 7, 7, 7], [7, 7, 7], list()) == (
        [
            True,
            True,
            True,
        ],
        [7],
        [],
    )

    assert compare_pairs([], [3], list()) == ([], [], [3])

    assert compare_pairs([[[]]], [[]], list()) == ([False], [], [])

    assert compare_pairs(
        [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
        [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
        list(),
    ) == ([True, True, True, True, True, True, False, True, True], [], [])


def test_part_1():
    data = process_input(os.path.join(base_path, "example.txt"))
    assert part_1(data) == 13


def test_part_2():
    data = process_input(os.path.join(base_path, "example.txt"))
    assert part_2(data) == 140
