import pytest

from .graph import GridWithWeights, SimpleGraph


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


@pytest.fixture()
def example_weighted_graph():
    graph = GridWithWeights(10, 10)
    graph.walls = [(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8)]
    graph.weights = {
        loc: 5
        for loc in [
            (3, 4),
            (3, 5),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 4),
            (4, 5),
            (4, 6),
            (4, 7),
            (4, 8),
            (5, 1),
            (5, 2),
            (5, 3),
            (5, 4),
            (5, 5),
            (5, 6),
            (5, 7),
            (5, 8),
            (6, 2),
            (6, 3),
            (6, 4),
            (6, 5),
            (6, 6),
            (6, 7),
            (7, 3),
            (7, 4),
            (7, 5),
        ]
    }
    return graph


def test_simple_graph(example_graph):
    assert example_graph.neighbors("A") == ["B"]
    assert example_graph.neighbors("D") == ["C", "E"]
    assert example_graph.neighbors("F") == []


def test_weighted_graph(example_weighted_graph):
    assert list(example_weighted_graph.neighbors((0, 0))) == [(0, 1), (1, 0)]
    assert example_weighted_graph.weights[(3, 4)] == 5
