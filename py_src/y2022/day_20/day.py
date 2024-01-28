from copy import deepcopy
import os
from pathlib import Path
from typing import List
from collections import deque

base_path = Path(__file__).parent

InputData = List[str]
Sorted = deque[tuple[int, int]]


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        return [int(line) for line in reader.read().splitlines()]


def find_start_index(data: Sorted) -> int:
    for i, v in enumerate(data):
        if v[1] == 0:
            return i
    raise ValueError("No start index found")


def calculate_result(data: Sorted, start: int) -> int:
    return sum(data[(start + offset) % len(data)][1] for offset in (1000, 2000, 3000))


# https://github.com/terminalmage/adventofcode/blob/main/2022/day20.py
def part_1(data: InputData) -> int:
    original_order = list(enumerate(int(x) * 1 for x in data))
    sorted_list: Sorted = deque(original_order, maxlen=len(data))
    for val in original_order:
        sorted_list.rotate(-sorted_list.index(val))
        sorted_list.rotate(-sorted_list.popleft()[1])
        sorted_list.appendleft(val)

    start_index = find_start_index(sorted_list)

    return calculate_result(sorted_list, start_index)


def part_2(data: InputData) -> int:
    return 0


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 9866

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
