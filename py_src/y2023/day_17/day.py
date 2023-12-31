from copy import deepcopy
import os
from pathlib import Path
from functools import partial
from typing import Generator, List, Optional, Iterator
from py_src.shared.graph import SquareGrid, GridLocation, WeightedGraph, Location
from py_src.shared.queue_1 import PriorityQueue

base_path = Path(__file__).parent

Direction = tuple[int, int]
State = tuple[int, Location, Direction]
CameFromMap = dict[Location, Optional[Location]]

EAST: Direction = (1, 0)
WEST: Direction = (-1, 0)
NORTH: Direction = (0, -1)
SOUTH: Direction = (0, 1)
START: Location = (0, 0)

VERTICALS = {NORTH, SOUTH}
HORIZONTALS = {WEST, EAST}


class HeatLossGrid(SquareGrid):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.weights: dict[GridLocation, float] = {}

    def cost(
        self,
        current_direction: Direction,
        span: int,
        from_node: GridLocation,
        to_node: GridLocation,
    ) -> float:
        cost = self.weights.get(to_node)
        return cost

    def passable(
        self,
        direction: Direction,
        span: int,
        from_node: GridLocation,
        to_node: GridLocation,
    ) -> bool:
        new_direction = self.get_direction(from_node, to_node)
        print(
            f"dir: direction: {direction} new_direction: {new_direction} span: {span}"
        )
        if direction == new_direction and span + 1 == 3:
            print("too much")
            return False

        # can't reverse
        if direction in VERTICALS and new_direction[1] == -direction[1]:
            return False

        if direction in HORIZONTALS and new_direction[0] == -direction[0]:
            return False

        # print(
        #     f"passable: direction: {direction}, new_direction: {new_direction} from_node: {from_node}, to_node: {to_node} span: {span}"
        # )

        return True

    def neighbors(
        self, id: GridLocation, direction: Direction, span: int
    ) -> Iterator[GridLocation]:
        is_traversable_direction_fn = partial(self.passable, direction, span, id)
        (x, y) = id
        neighbors = []
        neighbors = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]  # E W N S
        # straight = (x + direction[0], y + direction[1])
        # if direction != START:
        #     neighbors.append(straight)

        # if direction in VERTICALS or direction == START:
        #     neighbors = neighbors + [(x + 1, y), (x - 1, y)]

        # if direction in HORIZONTALS or direction == START:
        #     neighbors = neighbors + [(x, y - 1), (x, y + 1)]

        # print(f"straight: {straight} neighbors: {neighbors}")

        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0:
            neighbors.reverse()  # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(is_traversable_direction_fn, results)

        return results

    def add(_, position: Location, direction: Direction) -> Location:
        return (position[0] + direction[0], position[1] + direction[1])

    def get_reachable_states(
        self, position: Location, direction: Direction, cost: int
    ) -> List[State]:
        states = []
        states.extend(
            self.get_line_of_states(position, self.rotate_left(direction), cost)
        )
        states.extend(
            self.get_line_of_states(position, self.rotate_right(direction), cost)
        )

        return states

    def get_line_of_states(
        self, position: Location, direction: Direction, cost: int
    ) -> List[State]:
        neighbors = []
        for x, y in self.get_line_of_positions(position, direction):
            cost += self.weights.get((x, y), 0)
            neighbors.append((cost, (x, y), direction))

        return neighbors

    def get_line_of_positions(
        self, position: Location, direction: Direction
    ) -> List[Location]:
        adjacent = []
        for _ in range(3):
            position = self.add(position, direction)
            adjacent.append(position)

        return list(filter(self.in_bounds, adjacent))

    def rotate_left(_, direction: Direction) -> Direction:
        return (direction[1], -direction[0])

    def rotate_right(_, direction: Direction) -> Direction:
        return (-direction[1], direction[0])

    def get_direction(
        self, location: GridLocation, new_location: GridLocation
    ) -> GridLocation:
        return (new_location[0] - location[0], new_location[1] - location[1])


InputData = List[List[int]]


def reconstruct_path(
    came_from: CameFromMap, start: Location, goal: Location
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


def process_input(file: str) -> Generator[InputData, None, None]:
    with open(file, "r") as reader:
        for pairs in reader.read().split("\n\n"):
            yield list(
                map(
                    lambda val: [int(x) for x in val.strip()],
                    pairs.splitlines(),
                ),
            )


def heuristic(a: GridLocation, b: GridLocation) -> float:
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(graph: HeatLossGrid, start: Location, goal: Location):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: CameFromMap = {}
    cost_so_far: dict[Location, float] = {}
    came_from[start] = None
    current_direction = (0, 0)
    cost_so_far[start] = 0
    found = False
    span = 0
    # new_direction = (0, 0)

    while not frontier.empty():
        current: Location = frontier.get()
        new_direction = current_direction

        if current == goal and span < 3:
            found = True
            # print(f"here: {cost_so_far[current]}")
            break

        for next in graph.neighbors(current, current_direction, span):
            # if new_direction == current_direction and span == 3:
            #     span = 0
            #     continue

            new_cost = cost_so_far.get(current) + graph.cost(
                current_direction, span, current, next
            )
            new_direction = graph.get_direction(current, next)
            if new_direction == current_direction:
                span += 1
            else:
                span = 0

            # if new_cost > cost_so_far[next]:
            #     continue

            if next not in cost_so_far or new_cost < cost_so_far.get(next):
                # if current_direction == new_direction or current_direction == START:
                #     span += 1
                # print(
                #     f"current: {current}, next: {next} dir: {current_direction} {new_direction} {current_direction == new_direction} span: {span}"
                # )
                cost_so_far[next] = new_cost

                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current

            current_direction = new_direction

    return came_from, cost_so_far, found


def dijkstra(
    graph: HeatLossGrid, start: Location, goal: Location
) -> tuple[int, CameFromMap, bool]:
    frontier: State = PriorityQueue()
    frontier.put((0, start, EAST), (0, start, SOUTH))
    came_from: CameFromMap = {}
    came_from[start] = None
    visited = set()
    found = False

    while not frontier.empty():
        cost, current, current_direction = frontier.get()

        if (current, current_direction) in visited:
            continue

        visited.add((current, current_direction))

        if current == goal:
            found = True
            break

        for state in graph.get_reachable_states(current, current_direction, cost):
            new_cost, next_position, next_direction = state
            # priority = new_cost + heuristic(next_position, goal)
            frontier.put(state, new_cost)
            came_from[next_position] = current

    return came_from, cost, found


def part_1(data: InputData) -> int:
    rows = len(data)
    cols = len(data[0])
    graph: HeatLossGrid = HeatLossGrid(cols, rows)
    graph.edges = {}
    graph.weights = {}
    start_pos = (0, 0)
    end_pos = (rows - 1, cols - 1)

    for y, row in enumerate(data):
        for x, char in enumerate(row):
            elem = char
            graph.weights[(x, y)] = elem

    # came_from, cost_so_far, _ = a_star_search(graph, start_pos, end_pos)
    came_from, cost_so_far, _ = dijkstra(graph, start_pos, end_pos)

    # draw_grid(
    #     graph,
    #     path=reconstruct_path(came_from, start=start_pos, goal=end_pos),
    #     point_to=came_from,
    #     start=start_pos,
    #     goal=end_pos,
    # )

    return cost_so_far


def part_2(data: InputData) -> int:
    return 0


def main():
    pi = next(process_input(os.path.join(base_path, "input.txt")))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 963

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
