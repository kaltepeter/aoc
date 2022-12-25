from typing import Iterator, List, Protocol, Tuple, TypeVar

Location = TypeVar("Location")
GridLocation = Tuple[int, int]


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


class SquareGrid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.walls: list[GridLocation] = []

    def in_bounds(self, id: GridLocation) -> bool:
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id: GridLocation) -> bool:
        return id not in self.walls

    def neighbors(self, id: GridLocation) -> Iterator[GridLocation]:
        (x, y) = id
        neighbors = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]  # E W N S
        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0:
            neighbors.reverse()  # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return results


class GridWithWeights(SquareGrid):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.weights: dict[GridLocation, float] = {}

    def cost(self, from_node: GridLocation, to_node: GridLocation) -> float:
        return self.weights.get(to_node, 1)
