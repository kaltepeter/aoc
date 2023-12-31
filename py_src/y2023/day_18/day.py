from copy import deepcopy
import os
import pathlib
from typing import Generator, List
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np
import matplotlib.pyplot as plt

base_path = pathlib.Path(__file__).parent

InputData = List[tuple[str, float, str]]
Location = tuple[float, float]
Direction = tuple[float, float]

directions: dict[str, Direction] = {
    "R": (1.0, 0.0),
    "L": (-1.0, 0.0),
    "U": (0.0, -1.0),
    "D": (0.0, 1.0),
}


# http://philliplemons.com/posts/ray-casting-algorithm
# class Polygon:
#     def __init__(self, points: Location):
#         """
#         points: a list of Points in clockwise order.
#         """
#         self.points = points

#     @property
#     def edges(self):
#         """Returns a list of tuples that each contain 2 points of an edge"""
#         edge_list = []
#         for i, p in enumerate(self.points):
#             p1 = p
#             p2 = self.points[(i + 1) % len(self.points)]
#             edge_list.append((p1, p2))

#         return edge_list


def process_input(file: str) -> Generator[InputData, None, None]:
    with open(file, "r") as reader:
        for blocks in reader.read().split("\n\n"):
            lines = map(lambda val: val.strip(), blocks.splitlines())
            yield [
                (vals[0], float(vals[1]), vals[2].replace("(", "").replace(")", ""))
                for vals in [line.split(" ") for line in lines]
            ]


def part_1(data: InputData) -> int:
    rows = len(data)
    cols = len(data[0])
    codes = [Path.MOVETO]
    current_position: Direction = (0.0, 0.0)
    vertices = [current_position]

    for d, amount, color in data:
        direction = directions[d]
        move_amount = (direction[0] * amount, direction[1] * amount)
        current_position = (
            current_position[0] + move_amount[0],
            current_position[1] + move_amount[1],
        )
        vertices.append(current_position)
        codes.append(Path.LINETO)

    # Visual
    path: Path = Path(vertices, codes)
    fig, ax = plt.subplots()
    patch = patches.PathPatch(path, facecolor="orange", edgecolor="red", lw=2)
    ax.add_patch(patch)
    min_x = int(min([v[0] for v in vertices]))
    max_x = int(max([v[0] for v in vertices]))
    min_y = int(min([v[1] for v in vertices]))
    max_y = int(max([v[1] for v in vertices]))
    ax.set_xlim(-2, max_x + 2)
    ax.set_ylim(-2, max_y + 2)
    ax.invert_yaxis()

    # plt.show()

    count = 0
    for y in range(min_y - 1, max_y + 1):
        for x in range(min_x - 1, max_x + 1):
            # if inside or edge
            if path.contains_point((x, y)) or path.contains_point((x, y), radius=0.1):
                count += 1

    return count


def part_2(data: InputData) -> int:
    return 0


def main():
    pi = next(process_input(os.path.join(base_path, "input.txt")))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 35401

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
