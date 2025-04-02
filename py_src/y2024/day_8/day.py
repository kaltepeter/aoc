from copy import deepcopy
from itertools import combinations
import os
from pathlib import Path
from typing import Generator, List


base_path = Path(__file__).parent

# ({'0': [(8,1), (5, 2)]}, (12,12))
Coord = tuple[int, int]
InputData = tuple[dict[str, list[Coord]], tuple[int, int]]


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        for block in reader.read().split("\n\n"):
            grid = block.splitlines()
            antenna_list = {}
            for y, line in enumerate(grid):
                for x, c in enumerate(line):
                    if c != ".":
                        antenna_list.setdefault(c, []).append((x, y))

            return (antenna_list, (len(grid[0]), len(grid)))


# def find_aligned_pairs(coordinates):
#     pairs = []
#     for i, (x1, y1) in enumerate(coordinates):
#         for j, (x2, y2) in enumerate(coordinates[i+1:], i+1):
#             # If points have same x-coordinate (vertical line)
#             if x1 == x2:
#                 pairs.append(((x1,y1), (x2,y2)))
#             # If points have same y-coordinate (horizontal line)
#             elif y1 == y2:
#                 pairs.append(((x1,y1), (x2,y2)))
#             # If points form diagonal line
#             else:
#                 slope = (y2-y1)/(x2-x1)
#                 if slope.is_integer() or slope == 0:
#                     pairs.append(((x1,y1), (x2,y2)))
#     return pairs


def manhattan_distance(point1, point2):
    return sum(abs(a - b) for a, b in zip(point1, point2))


def in_bounds(position: Coord, max_x: int, max_y: int) -> bool:
    x, y = position
    return 0 <= x < max_x and 0 <= y < max_y


def part_1(data: InputData) -> int:
    antennas, (max_x, max_y) = data
    antinodes: set[Coord] = set()

    for antenna_list in antennas.values():
        pairs = combinations(antenna_list, 2)
        for pair in pairs:
            p1, p2 = pair
            next_coord_1 = tuple(a + (a - b) for a, b in zip(p1, p2))
            next_coord_2 = tuple(a + (a - b) for a, b in zip(p2, p1))

            if in_bounds(next_coord_1, max_x, max_y):
                antinodes.add(next_coord_1)

            if in_bounds(next_coord_2, max_x, max_y):
                antinodes.add(next_coord_2)

    return len(antinodes)


def part_2(data: InputData) -> int:
    antennas, (max_x, max_y) = data
    antinodes: set[Coord] = set()

    for antenna_list in antennas.values():
        pairs = combinations(antenna_list, 2)
        for pair in pairs:
            antinodes.update(pair)
            p1, p2 = pair

            path_1 = [p1, tuple(a + (a - b) for a, b in zip(p1, p2))]
            path_2 = [p2, tuple(a + (a - b) for a, b in zip(p2, p1))]

            while in_bounds(path_1[-1], max_x, max_y):
                antinodes.add(path_1[-1])
                path_1.append(tuple(a + (a - b) for a, b in zip(path_1[-1], path_1[-2])))

            while in_bounds(path_2[-1], max_x, max_y):
                antinodes.add(path_2[-1])
                path_2.append(tuple(a + (a - b) for a, b in zip(path_2[-1], path_2[-2])))


    return len(antinodes)


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 392

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 1235


if __name__ == "__main__":
    main()
