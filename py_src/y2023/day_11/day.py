from copy import deepcopy
import os
from pathlib import Path
from typing import List
import numpy as np
from itertools import combinations

# from py_src.shared.graph import Location, WeightedGraph, GridLocation, SquareGrid
# from py_src.shared.queue_1 import PriorityQueue
from functools import partial

base_path = Path(__file__).parent

InputData = List[str]
Coord = tuple[int, int]
# ({(x,y), (x,y)}, ([x, x], [y, y, y]))
GalaxyList = tuple[set[Coord], (List[int], List[int])]
GridLocation = tuple[int, int]


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        for lines in reader.read().split("\n\n"):
            return [line for line in lines.splitlines()]


# return a tuple of galaxies and empty rows and cols
def find_galaxies(data: InputData) -> GalaxyList:
    galaxies = set()
    x_list = [i for i in range(len(data[0]))]
    y_list = []

    for y, row in enumerate(data):
        if "#" not in row:
            y_list.append(y)

        for x, col in enumerate(row):
            if col == "#":
                if x in x_list:
                    x_list.remove(x)

                galaxies.add((x, y))

    return (galaxies, (x_list, y_list))


def expand_space(
    data: InputData, galaxy_list: GalaxyList, multiplier: int = 1
) -> InputData:
    _, (x_list, y_list) = galaxy_list
    for i, y in enumerate(y_list):
        expansion = i * multiplier
        row = data[y + expansion]
        data.insert(y + expansion, row)

    for i, x in enumerate(x_list):
        for y, row in enumerate(data):
            expansion = i * multiplier
            cur_col = x + expansion
            data[y] = row[:cur_col] + "." + row[cur_col:]

    return data


def calculate_galaxy_positions(galaxy_list: GalaxyList, multiplier: int = 2) -> int:
    galaxies, (x_list, y_list) = galaxy_list

    points = list(galaxies)
    total = 0

    for i, (r1, c1) in enumerate(points):
        for r2, c2 in points[:i]:
            for r in range(min(r1, r2), max(r1, r2)):
                total += multiplier if r in x_list else 1
            for c in range(min(c1, c2), max(c1, c2)):
                total += multiplier if c in y_list else 1

    return total


def heuristic(a: GridLocation, b: GridLocation) -> float:
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def part_1(data: InputData) -> int:
    galaxies = find_galaxies(data)
    expanded_galaxy = expand_space(data, galaxies)
    galaxies, _ = find_galaxies(expanded_galaxy)

    galaxy_pairs = set(combinations(galaxies, 2))

    return sum([heuristic(*pair) for pair in galaxy_pairs])


def part_2(data: InputData, multiplier: int = 2) -> int:
    galaxies = find_galaxies(data)

    return calculate_galaxy_positions(galaxies, multiplier)


def main():
    pi = list(process_input(os.path.join(base_path, "input.txt")))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 10231178

    part2_answer = part_2(deepcopy(pi), 1000000)
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 622120986954


if __name__ == "__main__":
    main()
