from copy import deepcopy
import os
from pathlib import Path
from typing import Generator, List, Union
import re

base_path = Path(__file__).parent

InputData = List[str]
Steps = List[tuple[str, str, int]]
# {box_num: {label: fs}}
LensList = dict[int, dict[str, int]]
# labels
Box = List[str]
REMOVE_LENS = "-"
REPLACE_OR_ADD = "="


def process_input(file: str) -> Generator[InputData, None, None]:
    with open(file, "r") as reader:
        for blocks in reader.read().split("\n\n"):
            res = list(map(lambda val: val.strip().split(","), blocks.splitlines()))
            assert len(res) == 1
            yield res[0]


def holiday_hash(val: str) -> int:
    result = 0
    for char in val:
        result += ord(char)
        result *= 17
        result = result % 256

    assert result > -1 and result < 256
    return result


def calculate_box_focus_power(box) -> int:
    result = 0

    return result


def part_1(data: InputData) -> int:
    results = []
    for seq in data:
        results.append(holiday_hash(seq))

    return sum(results)


def part_2(data: InputData) -> int:
    steps: Steps = [
        (s[0], s[1], int(s[2]) if s[2] else 0)
        for s in [re.split(r"(=|-){1}", step) for step in data]
    ]

    boxes = {}
    # boxes = {key: [] for key in range(0, 256)}
    lens_list: LensList = {}

    for step in steps:
        lb, operation, fs = step
        box = holiday_hash(lb)
        assert box > -1 and box < 256
        if box not in boxes:
            boxes[box] = []
        if box not in lens_list:
            lens_list[box] = {}

        if operation == REMOVE_LENS:
            if lb in boxes[box]:
                boxes[box].remove(lb)
            if lb in lens_list[box]:
                lens_list[box].pop(lb)

        else:
            lens_list[box][lb] = fs
            if lb not in boxes[box]:
                boxes[box].append(lb)

    result = 0
    for i, box in boxes.items():
        for slot, lens in enumerate(box):
            result += (1 + i) * (1 + slot) * lens_list[i][lens]
    return result


def main():
    pi = next(process_input(os.path.join(base_path, "input.txt")))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 501680

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 241094


if __name__ == "__main__":
    main()
