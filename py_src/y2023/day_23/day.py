from copy import deepcopy
from functools import partial
import os
from pathlib import Path
from typing import Iterator, List
from py_src.shared.graph import Location, SquareGrid, GridLocation, WeightedGraph

base_path = Path(__file__).parent

InputData = List[str]
hills = ["^", ">", "v", "<"]


class HikingTrailMap(SquareGrid):
    def __init__(self, width: int, height: int, data: InputData):
        super().__init__(width, height)
        self.weights: dict[GridLocation, float] = {}
        self.data = data

    def cost(self, from_node: GridLocation, to_node: GridLocation) -> float:
        return 1

    def in_bounds(self, id: GridLocation) -> bool:
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id: GridLocation) -> bool:
        return id not in self.walls

    def neighbors(self, id: GridLocation) -> Iterator[GridLocation]:
        (x, y) = id
        char = self.data[y][x]
        if char in hills:
            print(f"char: {char}")
            return []

        neighbors = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]  # E W N S
        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0:
            neighbors.reverse()  # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return results


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        data = reader.read().splitlines()
        return data


def dfs(graph, seen: set[Location], end: Location, pt: Location):
    if pt == end:
        return 0

    m = -float("inf")

    seen.add(pt)
    for nx in graph[pt]:
        if nx not in seen:
            m = max(m, dfs(graph, seen, end, nx) + graph[pt][nx])
    seen.remove(pt)

    return m


def part_1(data: InputData) -> int:
    rows = len(data)
    cols = len(data[0])
    start = (0, data[0].index("."))
    end = (rows - 1, data[-1].index("."))

    points: List[Location] = [start, end]

    graph = HikingTrailMap(cols, rows, data)
    graph.walls = []
    graph.data = data

    for r, row in enumerate(data):
        for c, ch in enumerate(row):
            if ch == "#":
                continue
            neighbors = 0
            for nr, nc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
                if 0 <= nr < rows and 0 <= nc < cols and data[nr][nc] != "#":
                    neighbors += 1
            if neighbors >= 3:
                points.append((r, c))

    graph = {pt: {} for pt in points}

    dirs = {
        "^": [(-1, 0)],
        "v": [(1, 0)],
        "<": [(0, -1)],
        ">": [(0, 1)],
        ".": [(-1, 0), (1, 0), (0, -1), (0, 1)],
    }

    for sr, sc in points:
        stack = [(0, sr, sc)]
        seen = {(sr, sc)}

        while stack:
            n, r, c = stack.pop()

            if n != 0 and (r, c) in points:
                graph[(sr, sc)][(r, c)] = n
                continue

            for dr, dc in dirs[data[r][c]]:
                nr = r + dr
                nc = c + dc
                if (
                    0 <= nr < rows
                    and 0 <= nc < cols
                    and data[nr][nc] != "#"
                    and (nr, nc) not in seen
                ):
                    stack.append((n + 1, nr, nc))
                    seen.add((nr, nc))

    return dfs(graph, set(), end, start)


def part_2(data: InputData) -> int:
    rows = len(data)
    cols = len(data[0])
    start = (0, data[0].index("."))
    end = (rows - 1, data[-1].index("."))

    points: List[Location] = [start, end]

    graph = HikingTrailMap(cols, rows, data)
    graph.walls = []
    graph.data = data

    for r, row in enumerate(data):
        for c, ch in enumerate(row):
            if ch == "#":
                continue
            neighbors = 0
            for nr, nc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
                if 0 <= nr < rows and 0 <= nc < cols and data[nr][nc] != "#":
                    neighbors += 1
            if neighbors >= 3:
                points.append((r, c))

    graph = {pt: {} for pt in points}

    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for sr, sc in points:
        stack = [(0, sr, sc)]
        seen = {(sr, sc)}

        while stack:
            n, r, c = stack.pop()

            if n != 0 and (r, c) in points:
                graph[(sr, sc)][(r, c)] = n
                continue

            for dr, dc in dirs:
                nr = r + dr
                nc = c + dc
                if (
                    0 <= nr < rows
                    and 0 <= nc < cols
                    and data[nr][nc] != "#"
                    and (nr, nc) not in seen
                ):
                    stack.append((n + 1, nr, nc))
                    seen.add((nr, nc))

    return dfs(graph, set(), end, start)


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 2134

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 6298


if __name__ == "__main__":
    main()
