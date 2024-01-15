from copy import deepcopy
import os
from pathlib import Path
from typing import List
import sympy

base_path = Path(__file__).parent

Coord = tuple[int, int, int]
InputData = List[tuple[Coord, Coord]]


class Hailstone:
    def __init__(self, sx, sy, sz, vx, vy, vz):
        self.sx = sx
        self.sy = sy
        self.sz = sz
        self.vx = vx
        self.vy = vy
        self.vz = vz

        self.a = vy
        self.b = -vx
        self.c = vy * sx - vx * sy

    def __repr__(self):
        return "Hailstone{" + f"a={self.a}, b={self.b}, c={self.c}" + "}"


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        lines = [tuple(line.split(" @ ")) for line in reader.read().splitlines()]
        return [
            (
                tuple(map(int, h.split(", "))),
                tuple(map(int, v.split(", "))),
            )
            for h, v in lines
        ]


def part_1(data: InputData, min_range=7, max_range=27) -> int:
    total = 0
    hailstones = [Hailstone(*h, *v) for h, v in data]

    # for i, hs1 in enumerate(data):
    #     for hs2 in data[:i]:
    #         px, py = sympy.symbols("px py")
    #         answers = sympy.solve(
    #             [
    #                 vy * (px - sx) - vx * (py - sy)
    #                 for (sx, sy, _), (vx, vy, _) in [hs1, hs2]
    #             ]
    #         )
    #         if len(answers) == 0:
    #             continue

    #         x, y = answers[px], answers[py]
    #         if min_range <= x <= max_range and min_range <= y <= max_range:
    #             if all(
    #                 (x - sx) * vx > 0 and (y - sy) * vy > -0
    #                 for (sx, sy, _), (vx, vy, _) in [hs1, hs2]
    #             ):
    #                 total += 1

    for i, hs1 in enumerate(hailstones):
        for hs2 in hailstones[:i]:
            a1, b1, c1 = hs1.a, hs1.b, hs1.c
            a2, b2, c2 = hs2.a, hs2.b, hs2.c
            if a1 * b2 == b1 * a2:
                continue
            x = (c1 * b2 - c2 * b1) / (a1 * b2 - a2 * b1)
            y = (c2 * a1 - c1 * a2) / (a1 * b2 - a2 * b1)
            if min_range <= x <= max_range and min_range <= y <= max_range:
                if all(
                    (x - hs.sx) * hs.vx >= 0 and (y - hs.sy) * hs.vy >= 0
                    for hs in (hs1, hs2)
                ):
                    total += 1

    return total


def part_2(data: InputData, min_range=7, max_range=27) -> int:
    xr, yr, zr, vxr, vyr, vzr = sympy.symbols("xr, yr, zr, vxr, vyr, vzr")
    equations = []

    for i, ((sx, sy, sz), (vx, vy, vz)) in enumerate(data):
        equations.append((xr - sx) * (vy - vyr) - (yr - sy) * (vx - vxr))
        equations.append((yr - sy) * (vz - vzr) - (zr - sz) * (vy - vyr))
        if i < 2:
            continue

        answers = [
            soln
            for soln in sympy.solve(equations)
            if all(x % 1 == 0 for x in soln.values())
        ]
        if len(answers) == 1:
            break

    answer = answers[0]

    return answer[xr] + answer[yr] + answer[zr]


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(
        deepcopy(pi), min_range=200000000000000, max_range=400000000000000
    )
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 15318

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 870379016024859


if __name__ == "__main__":
    main()
