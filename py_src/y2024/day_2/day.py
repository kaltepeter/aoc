from copy import deepcopy
import os
from pathlib import Path
from typing import List


base_path = Path(__file__).parent

InputData = List[List[int]]


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        for block in reader.read().split("\n\n"):
            return list(map(lambda val: list(map(int, val.split())), block.splitlines()))

def is_valid_ascending(numbers: List[int]) -> bool:
    return all(0 < b - a <= 3 for a, b in zip(numbers, numbers[1:]))

def is_valid_descending(numbers: List[int]) -> bool:
    return all(0 < a - b <= 3 for a, b in zip(numbers, numbers[1:]))

def part_1(data: InputData) -> int:
    count = 0

    for row in data:
        if is_valid_ascending(row):
            count += 1
        elif is_valid_descending(row):
            count += 1

    return count


def part_2(data: InputData) -> int:
    safe_list = []

    for row in data:
        variations = [row[:i] + row[i+1:] for i, _ in enumerate(row)]
        
        if any(is_valid_ascending(v) or is_valid_descending(v) for v in variations):
            safe_list.append(row)


    return len(safe_list)


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 549

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 589


if __name__ == "__main__":
    main()
