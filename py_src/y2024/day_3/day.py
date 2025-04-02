from copy import deepcopy
import os
from pathlib import Path
import re
from typing import Generator, List


base_path = Path(__file__).parent

InputData = str


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        for blocks in reader.read().split("\n\n"):
            return blocks


def part_1(data: InputData) -> int:
    nums = []
    total = 0

    multiply_commands = re.findall(r"mul\(\d{1,3}[\s,]\d{1,3}\)", data)
    for val in multiply_commands:
        x, y = map(int, re.findall(r"\d+", val))
        total += x * y

    return total


def part_2(data: InputData) -> int:
    total = 0
    sections = re.split(r"(don't\(\)|do\(\))", data)
    
    enabled = True
    for section in sections:
        if section == "don't()":
            enabled = False
        elif section == "do()":
            enabled = True
        elif enabled:
            multiply_commands = re.findall(r"mul\(\d{1,3}[s,]\d{1,3}\)", section)
            for val in multiply_commands:
                x, y = map(int, re.findall(r"\d+", val))
                total += x * y
    
    return total

def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 162813399

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 53783319


if __name__ == "__main__":
    main()
