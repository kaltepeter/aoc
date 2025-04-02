from copy import deepcopy
from itertools import product
import os
from pathlib import Path
from typing import List


base_path = Path(__file__).parent

InputData = List[str]


def process_input(file: str) -> InputData:
    result = []
    with open(file, "r") as reader:
        for blocks in reader.read().split("\n\n"):
            for line in blocks.splitlines():
                res, inputs = line.split(": ")
                result.append((int(res), list(map(int, inputs.split()))))

    return result


def evaluate_expression(nums: List[int], operators: List[str]) -> int:
    result = nums[0]
    for i in range(len(operators)):
        if operators[i] == '+':
            result += nums[i + 1]
        elif operators[i] == '*': 
            result *= nums[i + 1]
        else:
            result = int(f"{result}{nums[i + 1]}")

    return result


def part_1(data: InputData) -> int:
    valid = []
    for test_value, nums in data:
        for ops in product(['+', '*'], repeat=len(nums)-1):
            # print(f"test: {test_value}, nums: {nums}, ops: {ops}")
            if evaluate_expression(nums, ops) == test_value:
                valid.append(test_value)
                break

    return sum(valid)


def part_2(data: InputData) -> int:
    # TODO: slow, optimize by only using concat on negative cases?
    valid = []
    for test_value, nums in data:
        for ops in product(['+', '*', '||'], repeat=len(nums)-1):
            # print(f"test: {test_value}, nums: {nums}, ops: {ops}")
            if evaluate_expression(nums, ops) == test_value:
                valid.append(test_value)
                break

    return sum(valid)    


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 21572148763543

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 581941094529163


if __name__ == "__main__":
    main()
