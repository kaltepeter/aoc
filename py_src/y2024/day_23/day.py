from copy import deepcopy
from itertools import combinations
import os
from pathlib import Path
from typing import List
import networkx as nx
import matplotlib.pyplot as plt


base_path = Path(__file__).parent

Pair = tuple[str, str]
InputData = List[Pair]


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        block = reader.read().split("\n\n")[0]
        lines = block.splitlines()
        return [tuple(line.split("-")) for line in lines]
    

def build_graph(data: InputData) -> nx.Graph:
    G = nx.Graph()

    for pair in data:
        computer1, computer2 = pair
        G.add_node(computer1, label=computer1)
        G.add_node(computer2, label=computer2)
        G.add_edge(computer1, computer2)

    return G


def get_cliques_of_3_plus(G: nx.Graph) -> List[Pair]:
    return [clique for clique in nx.find_cliques(G) if len(clique) >= 3]


def filter_networks_start_with_t(networks: List[Pair]) -> List[Pair]:
    return [network for network in networks if any(node.startswith('t') for node in network)]


def part_1(G: nx.Graph) -> int:
    # nx.draw(G, with_labels=True, node_color='lightblue', font_weight='bold', font_size=14)
    # plt.show()

    networks = []
    cliques_of_3_plus = get_cliques_of_3_plus(G)
    cliques_of_3_plus = filter(filter_networks_start_with_t, cliques_of_3_plus)
    for clique in cliques_of_3_plus:
        if len(clique) > 3:
            networks.extend([c for c in combinations(clique, 3) if len(filter_networks_start_with_t([c])) > 0])
        else:
            networks.append(clique)

    unique_networks = {frozenset(network) for network in networks}

    # triads = [t for t in combinations(G, 3) if any(node.startswith('t') for node in t)]
    # type_300_triads = []
    # for triad in triads:
    #     triad = tuple(triad)
    #     if (G.has_edge(triad[0], triad[1]) and 
    #         G.has_edge(triad[1], triad[2]) and 
    #         G.has_edge(triad[0], triad[2])):
    #         type_300_triads.append(triad)

    # type_300_triads = {frozenset(triad) for triad in type_300_triads}

    
    return len(unique_networks)


def part_2(G: nx.Graph) -> str:
    largest_network = []

    cliques_of_3_plus = get_cliques_of_3_plus(G)
    cliques_of_3_plus = filter(filter_networks_start_with_t, cliques_of_3_plus)
    largest_network = max(cliques_of_3_plus, key=len)

    return ",".join(sorted(largest_network))


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))
    G = build_graph(deepcopy(pi))

    part1_answer = part_1(G)
    print(f"Part I: {part1_answer} \n")
    assert part1_answer < 2308
    assert part1_answer == 1400

    part2_answer = part_2(G)
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == "am,bc,cz,dc,gy,hk,li,qf,th,tj,wf,xk,xo"


if __name__ == "__main__":
    main()
