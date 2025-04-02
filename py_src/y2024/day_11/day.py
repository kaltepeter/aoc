from copy import deepcopy
import os
from pathlib import Path
from typing import List
from functools import cache


base_path = Path(__file__).parent

InputData = List[int]
Metric = List[dict[str, int]]


def split_number(num_str: str) -> tuple[int, int]:
    mid = len(num_str) // 2
    first_half = int(num_str[:mid])
    second_half = int(num_str[mid:])
    return first_half, second_half


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        for blocks in reader.read().split("\n\n"):
            line = blocks.splitlines()[0]
            return list(map(int, line.split()))


def blink(stones: List[int]) -> List[int]:
    new_stones = []
    for i, stone in enumerate(stones):
        stone_str = str(stone)

        if stone == 0:
            new_stones.append(1)
        elif len(stone_str) % 2 == 0:
            left, right = split_number(stone_str)
            new_stones.append(left)
            new_stones.append(right)
        else:
            new_stones.append(stone * 2024)

    return new_stones


@cache
def count_stones(stone: int, steps: int) -> int:
    if steps == 0:
        return 1
    if stone == 0:
        return count_stones(1, steps - 1)
    stone_str = str(stone)
    stone_len = len(stone_str)
    if stone_len % 2 == 0:
        left, right = split_number(stone_str)
        return count_stones(left, steps - 1) + count_stones(right, steps - 1)
    else:
        return count_stones(stone * 2024, steps - 1)


def part_1(data: InputData, blinks: int) -> int:
    stones = deepcopy(data)
    for _ in range(blinks):
        stones = blink(stones)

    return len(stones)


def part_2(data: InputData, blinks: int) -> int:
    return sum(count_stones(stone, blinks) for stone in data)


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi), 25)
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 213625

    part2_answer = part_2(deepcopy(pi), 75)
    print(f"Part II: {part2_answer} \n")
    assert part2_answer < 259094164889525 
    assert part2_answer == 252442982856820


if __name__ == "__main__":
    main()
