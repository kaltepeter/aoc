from copy import deepcopy
from functools import reduce
import os
from pathlib import Path
from typing import List
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

base_path = Path(__file__).parent

InputData = dict[str, set[str]]


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        pairs = [
            (k, set(v.split(" ")))
            for k, v in [line.split(": ") for line in reader.read().splitlines()]
        ]
        connections = {}
        for k, vals in pairs:
            if k not in connections:
                connections[k] = set()

            for v in vals:
                connections[k].add(v)
                if v not in connections:
                    connections[v] = set()

                connections[v].add(k)

        return connections


def part_1(data: InputData) -> int:
    vertices = []
    edges = []

    for k, vals in data.items():
        vertices.append(k)
        for v in vals:
            edges.append((k, v))

    G = nx.Graph()
    G.add_nodes_from(vertices)
    G.add_edges_from(edges)
    plt.subplot()
    nx.draw(G, with_labels=True, node_color="y", node_size=800)

    cuts = nx.minimum_edge_cut(G)
    for cut in cuts:
        G.remove_edge(*cut)

    # print(max(nx.connected_components(G), key=len))
    subgraphs = [G.subgraph(c).copy() for c in nx.connected_components(G)]
    counts = [len(s) for s in subgraphs]
    # plt.show()

    # num of cuts
    # print(nx.node_connectivity(G))
    # print(nx.minimum_edge_cut(G))
    # print(nx.cut_size(G))

    return np.multiply(*counts)


def part_2(data: InputData) -> int:
    return 0


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 613870

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
