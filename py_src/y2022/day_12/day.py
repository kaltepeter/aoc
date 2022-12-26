from copy import deepcopy
from functools import partial
import os

from pathlib import Path
from typing import Generator, Iterator, List, Optional, Tuple

from py_src.shared.graph import Location, SquareGrid, GridLocation, WeightedGraph
from py_src.shared.queue_1 import PriorityQueue

base_path = Path(__file__).parent


def reconstruct_path(
    came_from: dict[Location, Location], start: Location, goal: Location
) -> list[Location]:

    current: Location = goal
    path: list[Location] = []
    if goal not in came_from:  # no path was found
        return []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)  # optional
    path.reverse()  # optional
    return path


def draw_tile(graph, id, style):
    r = " . "
    if "number" in style and id in style["number"]:
        r = " %-2d" % style["number"][id]
    if "point_to" in style and style["point_to"].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style["point_to"][id]
        if x2 == x1 + 1:
            r = " > "
        if x2 == x1 - 1:
            r = " < "
        if y2 == y1 + 1:
            r = " v "
        if y2 == y1 - 1:
            r = " ^ "
    if "path" in style and id in style["path"]:
        r = " @ "
    if "start" in style and id == style["start"]:
        r = " S "
    if "goal" in style and id == style["goal"]:
        r = " E "
    if id in graph.walls:
        r = "###"
    return r


def draw_grid(graph, **style):
    print("___" * graph.width)
    for y in range(graph.height):
        for x in range(graph.width):
            print("%s" % draw_tile(graph, (x, y), style), end="")
        print()
    print("~~~" * graph.width)


class HeightMapGrid(SquareGrid):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.weights: dict[GridLocation, float] = {}

    def cost(self, from_node: GridLocation, to_node: GridLocation) -> float:
        return 1

    def passable(
        self,
        from_node: GridLocation,
        to_node: GridLocation,
    ) -> bool:
        from_value = self.weights.get(from_node, 0)
        to_value = self.weights.get(to_node, 0)
        delta = to_value - from_value
        return from_value == 0 or delta <= MAX_HEIGHT_DIFF

    def neighbors(self, id: GridLocation) -> Iterator[GridLocation]:
        is_acceptable_height_fn = partial(self.passable, id)
        (x, y) = id
        neighbors = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]  # E W N S
        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0:
            neighbors.reverse()  # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(is_acceptable_height_fn, results)
        return results


InputData = Tuple[HeightMapGrid, Location, Location]
MAX_HEIGHT_DIFF = 1
START_CHAR = "S"
END_CHAR = "E"


def get_printable_graph(
    data: InputData, rowCount: int, colCount: int
) -> Generator[str, None, None]:
    graph, start_pos, end_pos = data

    for y in range(start_pos[1], rowCount):
        for x in range(start_pos[0], colCount):
            if (x, y) == start_pos:
                yield START_CHAR
            elif (x, y) == end_pos:
                yield END_CHAR
            elif (x, y) in graph.weights:
                yield chr(graph.weights[(x, y)])
            else:
                yield "."
        yield "\n"


def print_graph(data: InputData, rowCount: int, colCount: int):
    for i in get_printable_graph(data, rowCount, colCount):
        print(i, end="")
    return data


def process_input(file: str) -> InputData:
    with open(file) as reader:
        lines = reader.read().strip().split("\n")
        rows = len(lines)
        cols = len(lines[0])

        graph = HeightMapGrid(cols, rows)
        graph.edges = {}
        graph.weights = {}
        start_pos = None
        end_pos = None

        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                elem = char

                if char == START_CHAR:
                    start_pos = (x, y)
                elif char == END_CHAR:
                    end_pos = (x, y)
                    graph.weights[(x, y)] = 123
                else:
                    elem = ord(char)
                    graph.weights[(x, y)] = elem

    data = (graph, start_pos, end_pos)
    # print_graph(data, rows, cols)
    return data


def heuristic(a: GridLocation, b: GridLocation) -> float:
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(graph: WeightedGraph, start: Location, goal: Location):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: dict[Location, Optional[Location]] = {}
    cost_so_far: dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0
    found = False

    while not frontier.empty():
        current: Location = frontier.get()

        if current == goal:
            found = True
            # print(f"here: {cost_so_far[current]}")
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far, found


def part_1(data: InputData) -> int:
    graph, start_pos, end_pos = data
    came_from, cost_so_far, _ = a_star_search(graph, start_pos, end_pos)
    # print(cost_so_far)
    # print(came_from)

    # draw_grid(
    #     graph,
    #     path=reconstruct_path(came_from, start=start_pos, goal=end_pos),
    #     point_to=came_from,
    #     start=start_pos,
    #     goal=end_pos,
    # )
    return cost_so_far.popitem()[1]


def get_a_locations(graph: HeightMapGrid) -> List[Location]:
    return [key for key, val in graph.weights.items() if val == ord("a")]

    while not frontier.empty():
        current: Location = frontier.get()

        if current == goal:
            found = True
            # print(f"here: {cost_so_far[current]}")
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far, found


def part_1(data: InputData) -> int:
    graph, start_pos, end_pos = data
    came_from, cost_so_far, _ = a_star_search(graph, start_pos, end_pos)
    # print(cost_so_far)
    # print(came_from)

    # draw_grid(
    #     graph,
    #     path=reconstruct_path(came_from, start=start_pos, goal=end_pos),
    #     point_to=came_from,
    #     start=start_pos,
    #     goal=end_pos,
    # )
    return cost_so_far.popitem()[1]


def get_a_locations(graph: HeightMapGrid) -> List[Location]:
    return [key for key, val in graph.weights.items() if val == ord("a")]


def part_2(data: InputData) -> int:
    graph, _, end_pos = data
    a_locations = get_a_locations(graph)
    distances = []

    for start_pos in a_locations:
        came_from, cost_so_far, found = a_star_search(graph, start_pos, end_pos)
        res = cost_so_far.popitem()[1]
        if found:
            # print(f"res: {res} found: {found}")
            distances.append(res)

    return min(distances)


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} shortest path\n")
    assert part1_answer == 352

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} shortest path\n")
    assert part2_answer == 345


if __name__ == "__main__":
    main()
