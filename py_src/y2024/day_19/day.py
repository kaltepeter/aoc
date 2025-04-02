from copy import deepcopy
import os
from pathlib import Path
from typing import List
from itertools import combinations, groupby


base_path = Path(__file__).parent

TowelPatterns = List[str]
InputData = tuple[TowelPatterns, List[str]]


def process_input(file: str) -> InputData:
    available_towels = []
    towel_patterns = []
    with open(file, "r") as reader:
        a, p = reader.read().split("\n\n")
        available_towels = a.split(', ')
        towel_patterns = p.splitlines()

    return (available_towels, towel_patterns)


def can_form_pattern(pattern: str, available_towels: List[str], start_pos: int = 0, memo={}) -> bool:
    key = (pattern, start_pos)
    if key in memo:
        return memo[key]

    if start_pos == len(pattern):
        return True

    for towel in available_towels:
        if pattern[start_pos:].startswith(towel):
            if can_form_pattern(pattern, available_towels, start_pos + len(towel), memo):
                memo[key] = True
                return True

    memo[key] = False
    return False


def compute_design_combos(pattern: str, available_towels: List[str], start_pos: int = 0, memo={}) -> int:
    key = (pattern, start_pos)
    if key in memo:
        return memo[key]

    if start_pos == len(pattern):
        return 1

    total = 0
    for towel in available_towels:
        if pattern[start_pos:].startswith(towel):
            total += compute_design_combos(pattern, available_towels, start_pos + len(towel), memo)

    memo[key] = total
    return total
    


def part_1(data: InputData) -> int:
    available_towels, towel_patterns = data
    count = 0

    for pattern in towel_patterns:
        if can_form_pattern(pattern, available_towels):
            count += 1


    return count


def part_2(data: InputData) -> int:
    available_towels, towel_patterns = data
    counts = []

    for pattern in towel_patterns:
        counts.append(compute_design_combos(pattern, available_towels))

    return sum(counts)


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer < 343
    assert part1_answer == 317

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 883443544805484


if __name__ == "__main__":
    main()
