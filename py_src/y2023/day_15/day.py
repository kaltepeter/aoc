from copy import deepcopy
import os
from pathlib import Path
from typing import Generator, List


base_path = Path(__file__).parent

InputData = List[str]


def process_input(file: str) -> Generator[InputData, None, None]:
    with open(file, "r") as reader:
        for blocks in reader.read().split("\n\n"):
            res = list(map(lambda val: val.strip().split(","), blocks.splitlines()))
            assert len(res) == 1
            yield res[0]


def holiday_hash(val: str) -> int:
    result = 0
    for char in val:
        result += ord(char)
        result *= 17
        result = result % 256

    assert result > -1 and result < 256
    return result


def part_1(data: InputData) -> int:
    results = []
    for seq in data:
        results.append(holiday_hash(seq))

    return sum(results)


def part_2(data: InputData) -> int:
    return 0


def main():
    pi = next(process_input(os.path.join(base_path, "input.txt")))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 501680

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
