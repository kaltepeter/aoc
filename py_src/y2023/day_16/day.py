from copy import deepcopy
import os
from pathlib import Path
from typing import Generator, List
from collections import deque

base_path = Path(__file__).parent

EMPTY = "."
FORWARD_MIRROR = "/"
BACK_MIRROR = "\\"
PIPE = "|"
DASH = "-"

InputData = List[str]


def process_input(file: str) -> Generator[InputData, None, None]:
    with open(file, "r") as reader:
        for blocks in reader.read().split("\n\n"):
            yield list(map(lambda val: val.strip(), blocks.splitlines()))


def fire_beam(data: InputData, row: int, col: int, dir_row: int, dir_col: int) -> int:
    start = [(row, col, dir_row, dir_col)]
    seen = set()
    q = deque(start)

    while q:
        row, col, dir_row, dir_col = q.popleft()

        row += dir_row
        col += dir_col

        if row < 0 or row >= len(data) or col < 0 or col >= len(data[0]):
            continue

        char = data[row][col]

        if (
            char == EMPTY
            or (char == DASH and dir_col != 0)
            or (char == PIPE and dir_row != 0)
        ):
            if (row, col, dir_row, dir_col) not in seen:
                seen.add((row, col, dir_row, dir_col))
                q.append((row, col, dir_row, dir_col))
        elif char == FORWARD_MIRROR:
            dir_row, dir_col = -dir_col, -dir_row
            if (row, col, dir_row, dir_col) not in seen:
                seen.add((row, col, dir_row, dir_col))
                q.append((row, col, dir_row, dir_col))
        elif char == BACK_MIRROR:
            dir_row, dir_col = dir_col, dir_row
            if (row, col, dir_row, dir_col) not in seen:
                seen.add((row, col, dir_row, dir_col))
                q.append((row, col, dir_row, dir_col))
        else:
            for dir_row, dir_col in (
                [(1, 0), (-1, 0)] if char == PIPE else [(0, 1), (0, -1)]
            ):
                if (row, col, dir_row, dir_col) not in seen:
                    seen.add((row, col, dir_row, dir_col))
                    q.append((row, col, dir_row, dir_col))

    results = {(row, col) for (row, col, _, _) in seen}

    return len(results)


def part_1(data: InputData) -> int:
    result = fire_beam(data, 0, -1, 0, 1)
    return result


def part_2(data: InputData) -> int:
    max_val = 0

    for row in range(len(data)):
        max_val = max(max_val, fire_beam(data, row, -1, 0, 1))
        max_val = max(max_val, fire_beam(data, row, len(data[0]), 0, -1))

    for col in range(len(data[0])):
        max_val = max(max_val, fire_beam(data, -1, col, 1, 0))
        max_val = max(max_val, fire_beam(data, len(data), col, -1, 0))

    return max_val


def main():
    pi = next(process_input(os.path.join(base_path, "input.txt")))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 7185

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 7616


if __name__ == "__main__":
    main()
