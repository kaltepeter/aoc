from copy import deepcopy
import os
from pathlib import Path
from typing import Generator, List


base_path = Path(__file__).parent

InputData = List[str]


def process_input(file: str) -> Generator[InputData, None, None]:
    with open(file, "r") as reader:
        for pairs in reader.read().split("\n\n"):
            yield list(map(lambda val: val.strip(), pairs.splitlines()))


def part_1(data: InputData) -> int:
    return 0


def part_2(data: InputData) -> int:
    return 0


def main():
    pi = next(process_input(os.path.join(base_path, "input.txt")))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 0

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
