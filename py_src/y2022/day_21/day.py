from copy import deepcopy
import os
from pathlib import Path
from typing import List

base_path = Path(__file__).parent

InputData = List[str]


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        data: InputData = {}
        for line in reader.read().splitlines():
            key, value = line.split(": ")
            data[key] = int(value) if value.isnumeric() else value

    return data


def part_1(data: InputData) -> int:
    values: dict[str, int] = {}
    keys_to_process = []
    for key, value in data.items():
        if isinstance(value, int):
            values[key] = value
        else:
            keys = tuple(k for k in value.split(" "))
            keys_to_process.append((key, (keys[0], keys[2])))

    # both datasets split root by +, no need for fancy
    root_keys = tuple(k for k in data["root"].split(" + "))
    while True:
        if set(root_keys) <= set(values.keys()):
            break

        for key, keys in keys_to_process:
            can_process = set(keys) <= set(values.keys())
            if not can_process:
                continue

            value = eval(data[key], {}, {k: values[k] for k in keys})
            if not isinstance(value, (int, float, complex)):
                raise ValueError(f"Value is not int: {value}")

            values[key] = value
            keys_to_process.remove((key, keys))

    return int(values[root_keys[0]] + values[root_keys[1]])


def part_2(data: InputData) -> int:
    return 0


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 85616733059734

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
