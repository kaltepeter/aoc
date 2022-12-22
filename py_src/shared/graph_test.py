import pytest

from .graph import SimpleGraph


@pytest.fixture()
def example_graph():
    example_graph = SimpleGraph()
    example_graph.edges = {
        "A": ["B"],
        "B": ["C"],
        "C": ["B", "D", "F"],
        "D": ["C", "E"],
        "E": ["F"],
        "F": [],
    }
    yield example_graph


def test_simple_graph(example_graph):
    assert example_graph.neighbors("A") == ["B"]
    assert example_graph.neighbors("D") == ["C", "E"]
    assert example_graph.neighbors("F") == []
