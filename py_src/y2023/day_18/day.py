from copy import deepcopy
import os
import pathlib
from typing import Generator, List
from matplotlib.path import Path
from matplotlib.axes import Axes
import matplotlib.patches as patches
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms

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

digit_to_directions: dict[int, str] = {
    0: "R",
    1: "D",
    2: "L",
    3: "U",
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


def convert_hex(data: InputData) -> List[tuple[str, float]]:
    return [
        (digit_to_directions[int(hex[-1])], int(hex[1:6], 16)) for _, _, hex in data
    ]


def visualize(path: Path, min_x=0, min_y=0, max_x=1, max_y=1, scale=1) -> None:
    border_size = 10
    scale_transform = transforms.Affine2D().scale(scale)
    fig, ax = plt.subplots()
    patch = patches.PathPatch(path, facecolor="orange", edgecolor="red", lw=2)
    patch.set_transform(scale_transform + ax.transData)
    ax.add_patch(patch)

    ax.set_xlim(min_x - border_size, max_x + border_size)
    ax.set_ylim(min_y - border_size, max_y + border_size)
    ax.invert_yaxis()

    plt.show()


def calculate_points(path: Path, min_x=0, min_y=0, max_x=1, max_y=1, scale=1) -> int:
    count = 0
    for y in range(min_y - 1, max_y + 1):
        for x in range(min_x - 1, max_x + 1):
            # if inside or edge
            radius = 0.1 / scale
            if path.contains_point((x, y)) or path.contains_point(
                (x, y), radius=radius
            ):
                count += 1

    return count


# https://artofproblemsolving.com/wiki/index.php?title=Shoelace_Theorem
def calculate_area(vertices: List[Location]) -> int:
    vertices = list(reversed(vertices))
    # handle overflow
    return (
        abs(
            sum(
                vertices[i][0]
                * (vertices[i - 1][1] - vertices[(i + 1) % len(vertices)][1])
                for i in range(len(vertices))
            )
        )
        // 2
    )
    # ccw = list(reversed(vertices))
    # count = len(ccw)
    # sum1 = 0
    # sum2 = 0

    # for i in range(0, count - 1):
    #     sum1 += ccw[i][0] * ccw[i + 1][1]
    #     sum2 += ccw[i][1] * ccw[i + 1][0]

    #     sum1 += ccw[count - 1][0] * ccw[0][1]
    #     sum2 += ccw[0][0] * ccw[count - 1][1]

    # return abs(sum1 - sum2) / 2


# really good walkthrough: https://www.youtube.com/watch?v=UNimgm_ogrw
def calculate_points_picks(area: int, boundary_points: int) -> int:
    return area + (boundary_points // 2) + 1


def part_1(data: InputData) -> int:
    codes = [Path.MOVETO]
    current_position: Direction = (0.0, 0.0)
    vertices = [current_position]
    boundary_points = 0

    for d, amount, _ in data:
        direction = directions[d]
        boundary_points += amount
        move_amount = (direction[0] * amount, direction[1] * amount)
        current_position = (
            current_position[0] + move_amount[0],
            current_position[1] + move_amount[1],
        )
        vertices.append(current_position)
        codes.append(Path.LINETO)

    x_coords, y_coords = zip(*vertices)

    min_x = int(min(x_coords))
    max_x = int(max(x_coords))
    min_y = int(min(y_coords))
    max_y = int(max(y_coords))

    # min_x = int(min([v[0] for v in vertices]))
    # max_x = int(max([v[0] for v in vertices]))
    # min_y = int(min([v[1] for v in vertices]))
    # max_y = int(max([v[1] for v in vertices]))

    # Visual
    # path: Path = Path(vertices, codes)
    # visualize(path, min_x=min_x, min_y=min_y, max_x=max_x, max_y=max_y)
    # return calculate_points(path, min_x=min_x, min_y=min_y, max_x=max_x, max_y=max_y)
    area = calculate_area(vertices)

    return int(calculate_points_picks(area, boundary_points))


def part_2(data: InputData) -> int:
    current_position: Direction = (0.0, 0.0)
    vertices = [current_position]

    converted_hex = convert_hex(data)

    boundary_points = 0
    for d, amount in converted_hex:
        direction = directions[d]
        boundary_points += amount
        move_amount = (direction[0] * amount, direction[1] * amount)
        current_position = (
            current_position[0] + move_amount[0],
            current_position[1] + move_amount[1],
        )
        vertices.append(current_position)

    area = calculate_area(vertices)

    return int(calculate_points_picks(area, boundary_points))


def main():
    pi = next(process_input(os.path.join(base_path, "input.txt")))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 35401

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 48020869073824


if __name__ == "__main__":
    main()
