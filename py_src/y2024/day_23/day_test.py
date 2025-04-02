import os
from pathlib import Path

import pytest
from .day import build_graph, part_1, part_2, process_input

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))


def test_process_input(example_data):
    assert len(example_data) == 32
    assert ('kh', 'tc') in example_data


def test_part_1(example_data):
    G = build_graph(example_data)
    assert part_1(G) == 7 


def test_part_2(example_data):
    G = build_graph(example_data)
    assert part_2(G) == "co,de,ka,ta" 
