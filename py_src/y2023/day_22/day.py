from copy import deepcopy
import os
from pathlib import Path
from typing import List


base_path = Path(__file__).parent
Location = List[int]
FIRST_X = 0
LAST_X = 3
FIRST_Y = 1
LAST_Y = 4
FIRST_Z = 2
LAST_Z = 5


class Brick:
    def __init__(self, name: int, location: str):
        self.name: int = name
        self.location: Location = list(map(int, location.replace("~", ",").split(",")))

    def __repr__(self) -> str:
        return f"{self.location}"

    def overlaps(self, other):
        return max(self.location[FIRST_X], other.location[FIRST_X]) <= min(
            self.location[LAST_X], other.location[LAST_X]
        ) and max(self.location[FIRST_Y], other.location[FIRST_Y]) <= min(
            self.location[LAST_Y], other.location[LAST_Y]
        )

    def supports(self, other):
        return self.location[FIRST_Z] == other.location[LAST_Z] + 1


InputData = List[Brick]
State = dict[str, int]


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        return [Brick(i, line) for i, line in enumerate(reader.read().splitlines())]


def part_1(data: InputData) -> int:
    sorted_bricks = sorted(data, key=lambda brick: brick.location[FIRST_Z])

    for i, brick in enumerate(sorted_bricks):
        max_z = 1
        for check in sorted_bricks[:i]:
            if brick.overlaps(check):
                max_z = max(max_z, check.location[LAST_Z] + 1)
            brick.location[LAST_Z] -= brick.location[FIRST_Z] - max_z
            brick.location[FIRST_Z] = max_z

    sorted_bricks.sort(key=lambda brick: brick.location[FIRST_Z])

    k_supports_v = {i: set() for i in range(len(sorted_bricks))}
    v_supports_k = {i: set() for i in range(len(sorted_bricks))}

    for j, upper in enumerate(sorted_bricks, start=0):
        for i, lower in enumerate(sorted_bricks[:j]):
            if lower.overlaps(upper) and upper.supports(lower):
                k_supports_v[i].add(j)
                v_supports_k[j].add(i)

    total = 0

    for i in range(len(sorted_bricks)):
        if all(len(v_supports_k[j]) >= 2 for j in k_supports_v[i]):
            total += 1

    return total


def part_2(data: InputData) -> int:
    return 0


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer < 514
    assert part1_answer == 501

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
