from copy import deepcopy
import os
from pathlib import Path
from typing import List
from functools import reduce

base_path = Path(__file__).parent

InputData = List[List[int]]
StepList = dict[int, List[int]]
NextStepsList = dict[int, int]


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        for pairs in reader.read().split("\n\n"):
            return list(
                map(
                    lambda val: [int(i) for i in val.strip().split(" ")],
                    pairs.splitlines(),
                )
            )


def calculate_steps(steps: List[int]) -> List[int]:
    reduced = reduce(
        lambda acc, val: acc + [val[1] - steps[val[0] - 1]] if val[0] > 0 else acc,
        enumerate(steps),
        [],
    )
    # print(f"{steps} -> {reduced}\n")
    return reduced


def calculate_step_list(data: InputData) -> StepList:
    step_list = {}
    for i, history in enumerate(data):
        step_list[i] = [history]
        while True:
            steps = calculate_steps(history)
            step_list[i].append(steps)
            if all(x == 0 for x in steps):
                break
            history = steps
    return step_list


def get_next_steps(step_list: StepList, at_end: bool = True) -> NextStepsList:
    next_items = {}
    for key, histories in step_list.items():
        histories = reversed(histories)
        for i, history in enumerate(histories):
            if next_items.get(key) is None:
                next_items[key] = 0

            if i == 0:
                continue

            if at_end:
                next_items[key] += history[-1]
            else:
                next_items[key] = history[0] - next_items[key]

    return next_items


def part_1(data: InputData) -> int:
    step_list = calculate_step_list(data)
    next_items = get_next_steps(step_list)

    return sum(next_items.values())


def part_2(data: InputData) -> int:
    step_list = calculate_step_list(data)

    next_items = get_next_steps(step_list, False)

    return sum(next_items.values())


def main():
    pi = list(process_input(os.path.join(base_path, "input.txt")))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer < 2005352210
    assert part1_answer == 2005352194

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 1077


if __name__ == "__main__":
    main()
