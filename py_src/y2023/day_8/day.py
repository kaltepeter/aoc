from copy import deepcopy
import os
import re
from pathlib import Path
from typing import List
from itertools import cycle
from math import lcm
from functools import reduce

base_path = Path(__file__).parent

NodeList = dict[str, tuple[str, str]]
InputData = tuple[List[str], NodeList]


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        blocks = reader.read().split("\n\n")
        node_list = [
            re.search(r"(\w+) = \((\w+), (\w+)\)", line)
            for line in blocks[1].splitlines()
        ]
        nodes = {}
        for node in node_list:
            key, val_1, val_2 = node.groups()
            nodes[key] = (val_1, val_2)

        return (blocks[0].strip(), nodes)


def run_path(
    moves: str, nodes: NodeList, current_node: str = "AAA", is_ghost: bool = False
) -> int:
    move_count = 0
    for move in cycle(moves):
        side = 0 if move == "L" else 1
        current_node = nodes[current_node][side]
        move_count += 1
        if not is_ghost and current_node == "ZZZ":
            break
        elif is_ghost and current_node[-1] == "Z":
            break

    return move_count


def part_1(data: InputData) -> int:
    moves, nodes = data

    return run_path(moves, nodes)


# modified with https://todd.ginsberg.com/post/advent-of-code/2023/day8/ approach
def part_2(data: InputData) -> int:
    moves, nodes = data
    paths = list(filter(lambda key: key[-1] == "A", nodes.keys()))
    # end_count = 0
    # move_count = 1
    calculated_steps = {start: run_path(moves, nodes, start, True) for start in paths}

    # goes on and on and on, not sure if completes
    # for move in cycle(moves):
    #     for i, path in enumerate(paths):
    #         side = 0 if move == "L" else 1
    #         next_node = nodes[path][side]
    #         paths[i] = next_node
    #         if next_node[-1] == "Z":
    #             end_count += 1

    #         if i % 100 == 0:
    #             print(f"path: {path} next_path: {next_node} end_count: {end_count}")

    #     # print(f"end_count: {end_count} move_count: {move_count}")
    #     if end_count >= len(paths):
    #         break
    #     else:
    #         end_count = 0
    #     move_count += 1

    return reduce(lcm, calculated_steps.values())


def main():
    pi = list(process_input(os.path.join(base_path, "input.txt")))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 11309

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 13740108158591


if __name__ == "__main__":
    main()
