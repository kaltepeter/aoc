from copy import deepcopy
from itertools import groupby
import os
from pathlib import Path
from typing import List
import networkx as nx
from networkx import Graph

base_path = Path(__file__).parent

Coord = tuple[int, int]
InputData = Graph


def process_input(file: str) -> InputData:
    graph = nx.Graph()
    with open(file, "r") as reader:
        for row_idx, row in enumerate(reader.read().splitlines()):
            for col_idx, char in enumerate(row):
                # Add node with position and value
                graph.add_node((row_idx, col_idx), value=char)
                
                # Connect to adjacent same-value nodes
                for adj_pos in [(row_idx-1, col_idx), (row_idx, col_idx-1)]:
                    if adj_pos in graph and graph.nodes[adj_pos]['value'] == char:
                        graph.add_edge((row_idx, col_idx), adj_pos)
    return graph


def get_group_edges(group_nodes: set[Coord]) -> List[Coord]:
    perimeter = []
    
    for node in group_nodes:
        x, y = node
        neighbors = [
            (x+1, y),
            (x-1, y),
            (x, y+1),
            (x, y-1)
        ]
        
        for neighbor in neighbors:
            if neighbor not in group_nodes:
                perimeter.append(neighbor)
                
    return perimeter


def get_corners(node: Coord) -> List[Coord]:
    x, y = node
    return [
        (x - 0.5, y - 0.5), (x + 0.5, y - 0.5), (x + 0.5, y + 0.5), (x - 0.5, y + 0.5)
    ]


def get_corner_count(region: set[Coord]) -> int:
    corner_candidates = set()
    corners = 0
    
    for x, y in region:
        for cx, cy in get_corners((x, y)):
            corner_candidates.add((cx, cy))

    for cx, cy in corner_candidates:
        config = [(x,y) in region for x, y in get_corners((cx, cy))]
        count = sum(config)
        if count == 1:
            corners += 1
        elif count == 2:
            if config == [True, False, True, False] or config == [False, True, False, True]:
                corners += 2
        elif count == 3:
            corners += 1

    return corners


def part_1(graph: InputData) -> int:
    total = 0
    groups = {}
    for component in nx.connected_components(graph):
        value = graph.nodes[list(component)[0]]['value']
        if value not in groups:
            groups[value] = []
        groups[value].append(component)

    for group_list in groups.values():
        for group in group_list:
            area = len(group)
            perimeter = len(get_group_edges(group))
            total += area * perimeter

    return total


def part_2(graph: InputData) -> int:
    total = 0
    groups = {}
    for component in nx.connected_components(graph):
        value = graph.nodes[list(component)[0]]['value']
        if value not in groups:
            groups[value] = []
        groups[value].append(component)

    for group_list in groups.values():
        for group in group_list:
            area = len(group)
            corners = get_corner_count(group)
            total += area * corners

    return total


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 1363682

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 787680 


if __name__ == "__main__":
    main()
