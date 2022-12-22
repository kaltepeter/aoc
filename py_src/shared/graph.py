from typing import List, Protocol, TypeVar

Location = TypeVar("Location")


class Graph(Protocol):
    def neighbors(self, id: Location) -> List[Location]:
        pass


class SimpleGraph:
    def __init__(self):
        self.edges: dict[Location, list[Location]] = {}

    def neighbors(self, id: Location) -> list[Location]:
        return self.edges[id]


class WeightedGraph(Graph):
    def cost(self, from_id: Location, to_id: Location) -> float:
        pass
