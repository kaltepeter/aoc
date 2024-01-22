from copy import deepcopy
import os
from pathlib import Path
from typing import Generator, List
from collections import deque
from copy import deepcopy

base_path = Path(__file__).parent

InputData = List[str]
PatternMap = dict[str, List[int]]


def rotate90(grid: InputData):
    return ["".join(list(x)) for x in zip(*grid)]


def process_input(file: str) -> Generator[List[InputData], None, None]:
    with open(file, "r") as reader:
        for lines in reader.read().split("\n\n"):
            yield list(map(lambda val: val.strip(), lines.splitlines()))


def find_pairs(nums: List[int]) -> List[tuple[int, int]]:
    pairs = []
    nums.sort()

    for i in range(len(nums) - 1):
        if nums[i + 1] - nums[i] == 1:
            pairs.append((nums[i], nums[i + 1]))

    return pairs


def find_mirror(note: InputData) -> int:
    for r in range(1, len(note)):
        above = note[:r][::-1]
        below = note[r:]

        above = above[: len(below)]
        below = below[: len(above)]

        if above == below:
            return r

    return 0


def find_mirror_with_smudges(note: InputData) -> int:
    for r in range(1, len(note)):
        above = note[:r][::-1]
        below = note[r:]

        if (
            sum(
                sum(0 if a == b else 1 for a, b in zip(x, y))
                for x, y in zip(above, below)
            )
            == 1
        ):
            return r

    return 0


def find_mirrored_rows(note: InputData, start_pair: (int, int)) -> int:
    current_pairs = deque([start_pair])

    row_count = 0
    while current_pairs:
        x1, x2 = current_pairs.popleft()
        left_row = note[x1]
        right_row = note[x2]

        if left_row == right_row:
            row_count += 1
            if x1 - 1 >= 0 and x2 + 1 < len(note):
                current_pairs.append((x1 - 1, x2 + 1))
        else:
            row_count = 0
            continue

    if row_count == 0:
        return 0

    return start_pair[0] + 1
    # if min_x == 0:
    #     return start_pair[0] + 1
    # elif max_x == len(note) - 1:
    #     print("yo")
    #     return len(final_note)
    # return start_pair[0] + 1 if min_x == 0 else len(final_note)


def process_rows(note: InputData) -> int:
    patterns: PatternMap = {}
    for i, line in enumerate(note):
        if line not in patterns:
            patterns[line] = [i]
        else:
            patterns[line].append(i)

    row_count = 0
    for counts in patterns.values():
        pairs = find_pairs(counts)
        while pairs:
            start_pair = pairs.pop()
            row_count = find_mirrored_rows(note, start_pair)

    return row_count


def part_1(data: List[InputData]) -> int:
    row_count = 0
    col_count = 0
    for note in data:
        rotated_note = rotate90(note)
        col_count += find_mirror(rotated_note)
        row_count += find_mirror(note)

    return (row_count * 100) + col_count


def part_2(data: InputData) -> int:
    row_count = 0
    col_count = 0
    for note in data:
        rotated_note = rotate90(note)
        col_count += find_mirror_with_smudges(rotated_note)
        row_count += find_mirror_with_smudges(note)

    return (row_count * 100) + col_count


def main():
    pi = list(process_input(os.path.join(base_path, "input.txt")))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer > 30688
    assert part1_answer == 35210

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 31974


if __name__ == "__main__":
    main()
