from copy import deepcopy
import os
from pathlib import Path
from queue import Queue
from typing import List, Optional
import networkx as nx
from networkx import Graph

from py_src.shared.graph import WeightedGraph


base_path = Path(__file__).parent

Coord = tuple[int, int]


class LavaMap(WeightedGraph):
    def __init__(self, width: int, height: int):
        super().__init__()
        self.width = width
        self.height = height
        self.lava_map: dict[Coord, int] = {}
        self.trail_heads: List[Coord] = []

    def neighbors(self, node: Coord) -> List[Coord]:
        dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        result = []
        for dir in dirs:
            neighbor = (node[0] + dir[0], node[1] + dir[1])
            if 0 <= neighbor[0] < self.width and 0 <= neighbor[1] < self.height:
                result.append(neighbor)

        return result

    def passable(
        self,
        from_node: Coord,
        to_node: Coord,
    ) -> bool:
        to_node_value = self.lava_map.get(to_node)
        from_node_value = self.lava_map.get(from_node)

        return to_node_value - from_node_value == 1


InputData = Graph


# def process_input(file: str) -> InputData:
#     map = None
#     with open(file, "r") as reader:
#         for blocks in reader.read().split("\n\n"):
#             rows = blocks.splitlines()
#             map = LavaMap(len(rows[0]), len(rows))
#             for y, row in enumerate(rows):
#                 for x, col in enumerate(row):
#                     map.lava_map[(x, y)] = int(col)
#                     if col == "0":
#                         map.trail_heads.append((x, y))

#     return map


def process_input(file: str) -> InputData:
    G = nx.Graph()

    with open(file) as f:
        for y, line in enumerate(f):
            for x, value in enumerate(line.strip()):
                coord = (x, y)
                is_trail_head = value == "0"
                is_trail_end = value == "9"
                G.add_node(
                    coord,
                    value=int(value),
                    trail_head=is_trail_head,
                    trail_end=is_trail_end,
                )

    # Add edges between valid neighbors
    for node in G.nodes:
        x, y = node
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        for neighbor in neighbors:
            if neighbor in G:
                node_value = G.nodes[node]["value"]
                neighbor_value = G.nodes[neighbor]["value"]
                if neighbor_value - node_value == 1:
                    G.add_edge(node, neighbor)

    return G


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
        r = " A "
    if "goal" in style and id == style["goal"]:
        r = " Z "
    # if id in graph.walls: r = "###"
    return r


def draw_grid(graph, **style):
    print("___" * graph.width)
    for y in range(graph.height):
        for x in range(graph.width):
            print("%s" % draw_tile(graph, (x, y), style), end="")
        print()
    print("~~~" * graph.width)


def reconstruct_path(
    came_from: dict[Coord, Coord], start: Coord, goal: Coord
) -> list[Coord]:
    current: Coord = goal
    path: list[Coord] = []
    if goal not in came_from:  # no path was found
        return []

    while current != start:
        path.append(current)
        current = came_from[current]

    path.append(start)  # optional
    path.reverse()  # optional

    return path


def walk_trail(data: InputData, start: Coord) -> tuple[List[Coord], bool]:
    frontier = Queue()
    frontier.put(start)
    came_from: dict[Coord, Optional[Coord]] = {}
    came_from[start] = None

    while not frontier.empty():
        current: Coord = frontier.get()

        if data.lava_map.get(current) == 9:  # early exit
            trail_end_reached = True
            goal = current
            # break

        for next in data.neighbors(current):
            if next not in came_from and data.passable(current, next):
                frontier.put(next)
                came_from[next] = current

    draw_grid(
        data,
        path=reconstruct_path(came_from, start=start, goal=goal),
        point_to=came_from,
        start=start,
        goal=goal,
    )

    return (came_from, trail_end_reached)


def part_1(data: InputData) -> int:
    trail_heads = [node for node, attrs in data.nodes(data=True) if attrs['trail_head']]
    trail_ends = [node for node, attrs in data.nodes(data=True) if attrs['trail_end']]
    
    valid_paths = 0
    for start in trail_heads:
        # Get only trail_ends that are within 10 steps manhattan distance
        nearby_ends = [end for end in trail_ends 
                      if abs(end[0] - start[0]) + abs(end[1] - start[1]) <= 10]
        
        for end in nearby_ends:
            try:
                dist, path = nx.bidirectional_dijkstra(data, start, end)
                if len(path) == 10:
                    valid_paths += 1
            except nx.NetworkXNoPath:
                continue
            
    return valid_paths


def part_2(data: InputData) -> int:
    trail_heads = [node for node, attrs in data.nodes(data=True) if attrs['trail_head']]
    trail_ends = [node for node, attrs in data.nodes(data=True) if attrs['trail_end']]
    
    distinct_trails = set()
    for start in trail_heads:
        for end in trail_ends:
            paths = nx.all_simple_paths(data, start, end, cutoff=10)
            for path in paths:
                values = [data.nodes[node]['value'] for node in path]
                if values == list(range(10)):
                    distinct_trails.add(tuple(path))
                
    return len(distinct_trails)


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 652

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 1432 


if __name__ == "__main__":
    main()
