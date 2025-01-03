from collections import deque
from copy import deepcopy
from itertools import combinations, product
import os
from pathlib import Path
from typing import List


base_path = Path(__file__).parent

Locks = List[int]
Keys = List[int]
InputData = tuple[Locks, Keys, int]


def count_columns(data: List[str], is_key: bool) -> List[int]:
    col_count = len(data[0])
    counts = [0 for _ in range(col_count)]
    rows = deepcopy(data)
    if is_key:
        rows = data[::-1]

    for x in range(col_count):
        for y in range(len(rows)):
            char = rows[y][x]
            if char == '.':
                break
            if char == '#':
                counts[x] += 1

    
    return counts


def process_input(file: str) -> InputData:
    locks = []
    keys = []
    height = 0
    with open(file, "r") as reader:
        for blocks in reader.read().split("\n\n"):
            block = blocks.splitlines()
            height = len(block) - 1
            if len(block[0]) == block[0].count('#'):
                if '#' in block[-1]:
                    raise  ValueError("Invalid lock")
                locks.append(count_columns(block[1:], False))
            if len(block[-1]) == block[-1].count('#'):
                if '#' in block[0]:
                    raise ValueError("Invalid key")
                keys.append(count_columns(block[:-1], True))
                
    return (locks, keys, height)


def check_lock(lock: Locks, key: Keys, height: int) -> bool:
    for l, k in zip(lock, key):
        if l + k >= height:
            return False

    return True


def part_1(data: InputData) -> int:
    locks, keys, height = data
    count = 0
    combos = product(locks, keys)

    for lock, key in combos:
        if check_lock(lock, key, height):
            count += 1

    return count


def part_2(data: InputData) -> int:
    return 0


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 3269

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
