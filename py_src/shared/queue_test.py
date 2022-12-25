from queue import PriorityQueue

import pytest


@pytest.fixture()
def example_queue():
    example_queue = PriorityQueue()
    example_queue.put((0, 0), 0)
    example_queue.put((0, 1), 1)
    example_queue.put((1, 0), 1)
    return example_queue


def test_priority_queue_empty():
    example_queue = PriorityQueue()
    assert example_queue.empty()


def test_priority_queue_get(example_queue):
    assert example_queue.get() == (0, 0)
    example_queue.put((-1, 0))
    assert example_queue.get() == (-1, 0)
