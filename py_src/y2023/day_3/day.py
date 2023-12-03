from copy import deepcopy
import os
import re
from pathlib import Path
from typing import Generator, List


base_path = Path(__file__).parent

InputData = List[str]

EMPTY = "."


def process_input(file: str) -> Generator[InputData, None, None]:
    with open(file, "r") as reader:
        for lines in reader.read().split("\n"):
            yield lines


# bailed
def ranges_overlap(range1: tuple, range2: List[tuple]) -> bool:
    for r in range2:
        right_range = range(r[0] - 1, r[0] + 1)

        for i in range(range1[0] - 1, range1[1] + 1):
            if i in right_range:
                return True

    return False


def part_1(data: InputData) -> int:
    coords = set()
    grid = list(data)

    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch.isdigit() or ch == EMPTY:
                continue
            for cr in [r - 1, r, r + 1]:
                for cc in [c - 1, c, c + 1]:
                    if (
                        cr < 0
                        or cr >= len(grid)
                        or cc < 0
                        or cc >= len(grid[cr])
                        or not grid[cr][cc].isdigit()
                    ):
                        continue

                    while cc > 0 and grid[cr][cc - 1].isdigit():
                        cc -= 1
                    coords.add((cr, cc))

    part_numbers = []
    for row, col in coords:
        part_number = re.match(
            r"^(\d+)",
            grid[row][col:],
        )
        if part_number:
            part_numbers.append(int(part_number.group(1)))

    return sum(part_numbers)


def part_2(data: InputData) -> int:
    grid = list(data)

    gear_ratios = []

    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch != "*":
                continue

            coords = set()
            for cr in [r - 1, r, r + 1]:
                for cc in [c - 1, c, c + 1]:
                    if (
                        cr < 0
                        or cr >= len(grid)
                        or cc < 0
                        or cc >= len(grid[cr])
                        or not grid[cr][cc].isdigit()
                    ):
                        continue

                    while cc > 0 and grid[cr][cc - 1].isdigit():
                        cc -= 1
                    coords.add((cr, cc))

            if len(coords) == 2:
                part_numbers = []
                for row, col in coords:
                    part_number = re.match(
                        r"^(\d+)",
                        grid[row][col:],
                    )
                    if part_number:
                        part_numbers.append(int(part_number.group(1)))

                gear_ratios.append(part_numbers[0] * part_numbers[1])

    return sum(gear_ratios)


def main():
    pi = list(process_input(os.path.join(base_path, "input.txt")))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer > 104028
    assert part1_answer < 565910
    assert part1_answer < 532820
    assert part1_answer == 527144

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 81463996


if __name__ == "__main__":
    main()
