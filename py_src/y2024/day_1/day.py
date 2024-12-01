from copy import deepcopy
import os
from pathlib import Path
from typing import List
from collections import Counter

base_path = Path(__file__).parent

InputData = tuple[List[int], List[int]]


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        left, right = [], []
        # Read all pairs at once and split 
        pairs = [line.split() for block in reader.read().split("\n\n")
                 for line in block.splitlines()]
            
        # Unpack and convert to integers 
        left, right = zip(*((int(l), int(r)) for l, r in pairs))
            
        # Convert to lists and sort
        return (sorted(left), sorted(right))


def part_1(data: InputData) -> int:
    total_distance = 0

    for (l, r) in zip(*data):
        total_distance += abs(r - l)

    return total_distance


def part_2(data: InputData) -> int:
    similarity_score = 0
    right_counter = Counter(data[1])

    for num in data[0]:
        similarity_score += (num * right_counter[num])

    return similarity_score


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 1879048

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 21024792


if __name__ == "__main__":
    main()
