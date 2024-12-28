import os
from pathlib import Path

import pytest
from .day import find_cheats, get_cheats_saving_x_seconds, part_1, part_2, process_input

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    start, end, graph, walls, max_x, max_y = example_data
    assert len(graph.nodes) == 85
    assert start == (1, 3)
    assert end == (5, 7)
    assert len(walls) == 84
    assert max_x == 15
    assert max_y == 15


def test_find_cheats(example_data):
    _, _, graph, walls, max_x, max_y = example_data
    cheats = find_cheats(graph, walls)
    # for cheat in cheats:
    #     cheated_grid, cheated_walls = get_cheated_grid(graph, walls, cheat)
    #     # print_grid(cheated_grid, max_x, max_y, cheated_walls, path=None, cheat=None)
    
    assert len(cheats) == 72


def test_part_1(example_data):
    counts = part_1(example_data)
    assert counts[2] == 14
    assert counts[4] == 14
    assert counts[6] == 2
    assert counts[8] == 4
    assert counts[10] == 2
    assert counts[12] == 3
    assert counts[20] == 1
    assert counts[36] == 1
    assert counts[38] == 1
    assert counts[40] == 1
    assert counts[64] == 1


def test_cheats_saving_100_seconds(example_data):
    counts = part_1(example_data)
    assert get_cheats_saving_x_seconds(counts, 100) == 0
    assert get_cheats_saving_x_seconds(counts, 2) == 44


def test_part_2(example_data):
    assert part_2(example_data) == 0
