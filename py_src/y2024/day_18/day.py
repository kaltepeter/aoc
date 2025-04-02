from copy import deepcopy
import os
from pathlib import Path
from typing import List
import networkx as nx
from networkx import Graph


base_path = Path(__file__).parent

Coord = tuple[int, int]
InputData = tuple[Graph, List[Coord], int]


def process_input(file: str, max_size: int) -> InputData:
    G = nx.Graph()
    byte_list = []
    with open(file, "r") as reader:
        for block in reader.read().split("\n\n"):
            lines = block.splitlines()
            for line in lines:
                x,y = line.split(",")
                byte_list.append((int(x), int(y)))

    for i in range(max_size):
        for j in range(max_size):
            G.add_node((i, j))

    for node in G.nodes:
        x, y = node
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            neighbor = (x + dx, y + dy)
            if neighbor in G.nodes:
                G.add_edge(node, neighbor)


    return (G, byte_list, max_size)


def print_grid(grid: Graph, max_size: int, walls: List[Coord] = None, path: List[Coord] = None):
    walls = walls or []
    path = path or []
    for y in range(max_size):
        for x in range(max_size):
            if (x, y) in walls:
                print("#", end="")
            elif (x, y) in path:
                print("O", end="")
            else:
                print(".", end="")

        print()
    print()


def part_1(data: InputData, max_bytes: int) -> int:
    grid, byte_list, max_size = data

    if max_bytes > len(byte_list):
        raise ValueError("max_bytes is greater than the number of bytes in the input")

    path = None
    walls = []
    for node in byte_list[:max_bytes]:
        walls.append(node)

        for edge in list(grid.edges(node)):
            grid.remove_edge(*edge)

        path = nx.shortest_path(grid, source=(0, 0), target=(max_size-1, max_size-1))
        # print_grid(grid, max_size, walls, path)
    
    
    return len(path) - 1 # start doesn't count


def part_2(data: InputData) -> Coord:
    grid, byte_list, max_size = data

    walls = []
    node = None
    while byte_list:
        node = byte_list.pop(0)
        walls.append(node)

        for edge in list(grid.edges(node)):
            grid.remove_edge(*edge)

        try:
            nx.shortest_path(grid, source=(0, 0), target=(max_size-1, max_size-1))
        except nx.NetworkXNoPath:
            # print_grid(grid, max_size, walls, path)
            break
    
    return node


def main():
    pi = process_input(os.path.join(base_path, "input.txt"), 71)

    part1_answer = part_1(deepcopy(pi), 1024)
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 334

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == (20, 12)


if __name__ == "__main__":
    main()
