from copy import deepcopy
from itertools import groupby, repeat
import operator
import os
from pathlib import Path
import re
from typing import Generator, List


base_path = Path(__file__).parent

DiskCoord = tuple[int, int]
InputData = str


def process_input(file: str) -> Generator[InputData, None, None]:
    with open(file, "r") as reader:
        for block in reader.read().split("\n\n"):
            if block.startswith("//"):
                continue

            yield block.splitlines()[0]


def calculate_checksum(file_blocks: List[int]) -> int:
    return sum(i * x for i, x in enumerate(file_blocks))


def collect_disk_blocks(data: str) -> List[int]:
    disk_map = []
    last_id = 0

    for pos, key in enumerate(data):
        num = int(key)
        if pos % 2 == 0:
            disk_map += [last_id] * num
            last_id += 1
        else:
            disk_map += [-1] * num

    return disk_map


def map_disk_blocks(data: str) -> tuple[dict[int, DiskCoord], List[DiskCoord], int]:
    files = {}
    blanks = []

    last_id = 0
    pos = 0

    for i, char in enumerate(data):
        num = int(char)
        if i % 2 == 0:
            if num == 0:
                raise ValueError("Unexpected pos=0 for a file")
            
            files[last_id] = (pos, num)
            last_id += 1
        else:
            if num != 0:
                blanks.append((pos, num))

        pos += num

    return (files, blanks, last_id)


def part_1(data: InputData) -> int:
    disk_map = collect_disk_blocks(data)

    empty_blocks = [
        i for i, x in enumerate(disk_map) if x == -1
    ]

    for i in empty_blocks:
        while disk_map[-1] == -1:
            disk_map.pop()
        if len(disk_map) <= i:
            break

        disk_map[i] = disk_map.pop()

    return calculate_checksum(disk_map)


def part_2(data: InputData) -> int:
    files, blanks, last_id = map_disk_blocks(data)

    while last_id > 0:
        last_id -= 1
        pos, size = files[last_id]
        for i, (start, length) in enumerate(blanks):
            if start >= pos:
                blanks = blanks[:i]
                break
            
            if size <= length:
                files[last_id] = (start, size)
                if size == length:
                    blanks.pop(i)
                else:
                    blanks[i] = (start + size, length - size)

                break

    total = 0
    for fid, (pos, size) in files.items():
        for x in range(pos, pos + size):
            total += fid * x

    return total


def main():
    pi = next(process_input(os.path.join(base_path, "input.txt")))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 6432869891895

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 6467290479134


if __name__ == "__main__":
    main()
