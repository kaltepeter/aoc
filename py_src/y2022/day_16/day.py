import itertools
import os
import re
from copy import deepcopy
from pathlib import Path
from queue import PriorityQueue
from typing import Generator, List, Optional, Tuple

from py_src.shared.graph import WeightedGraph

base_path = Path(__file__).parent

Location = str

nV = 4

INF = 999


class PipeMap(WeightedGraph):
    def __init__(
        self,
    ):
        super().__init__()
        self.edges: dict[Location, list[Location]] = {}
        self.flows: dict[Location, int] = {}
        self.indicies: dict[Location, int] = {}
        self.distances: dict[Tuple(Location, Location), int] = {}

    def cost(self, from_node: Location, to_node: Location) -> float:
        return self.flows.get(to_node, 1)

    def neighbors(self, id: Location) -> List[Location]:
        return self.edges[id]

    def floyd_warshall(self) -> None:
        for k, i, j in itertools.permutations(self.edges, 3):
            # print(f"k: {k}, i: {i}, j: {j}")
            self.distances[i, j] = min(
                self.distances[i, j], self.distances[i, k] + self.distances[k, j]
            )


InputData = PipeMap


def process_input(file: str) -> InputData:
    pipe_map = PipeMap()
    with open(file, "r") as reader:
        for line in reader.read().split("\n"):
            info = re.findall(
                r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ([\w, ]+)",
                line,
            )
            if len(info) == 0:
                continue
            info = info[0]
            valve = info[0]
            flow_rate = int(info[1])
            tunnels = list(map(str.strip, info[2].split(",")))
            pipe_map.edges[valve] = tunnels
            if flow_rate != 0:
                pipe_map.flows[valve] = flow_rate
        pipe_map.indicies = {valve: 1 << i for i, valve in enumerate(pipe_map.flows)}
        pipe_map.distances = {
            (v, l): 1 if l in pipe_map.edges[v] else 1000
            for l in pipe_map.edges
            for v in pipe_map.edges
        }
    return pipe_map


def visit(data: PipeMap, valve: str, minutes: int, bitmask: int, pressure: int, answer):
    answer[bitmask] = max(answer.get(bitmask, 0), pressure)
    for valve2, flow in data.flows.items():
        remaining_minutes = minutes - data.distances[valve, valve2] - 1
        if remaining_minutes <= 0 or data.indicies[valve2] & bitmask:
            continue
        visit(
            data,
            valve2,
            remaining_minutes,
            bitmask | data.indicies[valve2],
            pressure + flow * remaining_minutes,
            answer,
        )
    return answer


def part_1(data: InputData) -> int:
    data.floyd_warshall()
    return max(visit(data, "AA", 30, 0, 0, {}).values())


def part_2(data: InputData) -> int:
    data.floyd_warshall()

    visited = visit(data, "AA", 26, 0, 0, {})
    return max(
        v1 + v2
        for bitm1, v1 in visited.items()
        for bitm2, v2 in visited.items()
        if not bitm1 & bitm2
    )


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 1595

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 2189


if __name__ == "__main__":
    main()
