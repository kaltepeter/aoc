import os
from pathlib import Path

from .day import part_1, process_input


base_path = Path(__file__).parent


def test_process_input():
    graph, start_pos, end_pos = process_input(os.path.join(base_path, "example.txt"))
    assert start_pos == (0, 0)
    assert end_pos == (5, 2)
    assert (0, 0) not in graph.weights
    assert graph.weights[(0, 1)] == ord("a")
    assert graph.weights[(1, 0)] == ord("a")
    assert graph.weights[(1, 1)] == ord("b")
    assert sorted(list(graph.neighbors((0, 0)))) == [(0, 1), (1, 0)]
    assert sorted(list(graph.neighbors((1, 2)))) == [(0, 2), (1, 1), (1, 3), (2, 2)]
    assert sorted(list(graph.neighbors((7, 4)))) == [(6, 4), (7, 3)]


def test_part_1():
    data = process_input(os.path.join(base_path, "example.txt"))
    assert part_1(data) == 31
