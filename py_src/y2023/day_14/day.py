from copy import deepcopy
import os
from pathlib import Path
from typing import Generator, List
import re

base_path = Path(__file__).parent

InputData = List[str]

ROLLING_ROCK = "O"
FLAT_ROCK = "#"
EMPTY = "."


def process_input(file: str) -> Generator[InputData, None, None]:
    with open(file, "r") as reader:
        for lines in reader.read().split("\n\n"):
            yield list(map(lambda val: val.strip(), lines.splitlines()))


def calculate_load(data: InputData) -> int:
    num_rows = len(data)
    result = 0
    for i, row in enumerate(data):
        count = row.count(ROLLING_ROCK)
        result += (num_rows - i) * count
        # for col in row:
        # if col == "O":
        # result += num_rows - i

    return result


def part_1(data: InputData) -> int:
    # rotated = ["".join(list(x)) for x in zip(*data)]
    # print("\n".join(rotated))
    # print("")
    # for ri, row in enumerate(rotated):
    #     print(ri, row)
    #     new_row = row[0]
    #     for ci in range(1, len(row)):
    #         for ci2 in range(ci, 0, -1):
    #             if row[ci] == "O" and row[ci2] == ".":
    #                 new_row += "O"
    #             else:
    #                 new_row += row[ci]

    #     print(ri, new_row)

    rotated_grid = list(map("".join, zip(*data)))
    tilted = [
        FLAT_ROCK.join(
            [
                "".join(sorted(list(group), reverse=True))
                for group in row.split(FLAT_ROCK)
            ]
        )
        for row in rotated_grid
    ]
    processed_data = list(map("".join, zip(*tilted)))
    return calculate_load(processed_data)


def part_2(data: InputData) -> int:
    return 0


def main():
    pi = list(process_input(os.path.join(base_path, "input.txt")))

    part1_answer = part_1(deepcopy(pi)[0])
    print(f"Part I: {part1_answer} \n")
    assert part1_answer < 108381
    assert part1_answer == 105623

    part2_answer = part_2(deepcopy(pi)[0])
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
