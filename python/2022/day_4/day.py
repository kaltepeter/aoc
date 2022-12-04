import os
from pathlib import Path
from typing import List, Tuple


base_path = Path(__file__).parent

Pairs = List[Tuple[Tuple[int, int], Tuple[int, int]]]


def process_input(file: str) -> Pairs:
    with open(file) as reader:
        data = reader.read().strip().split("\n")
        pair_data = [tuple(pair.split(",")) for pair in data]
        pairs = [
            (tuple(map(int, pair[0].split("-"))), tuple(map(int, pair[1].split("-"))))
            for pair in pair_data
        ]
        return pairs


def are_ranges_overlapping(range1: Tuple[int, int], range2: Tuple[int, int]) -> bool:
    if range1[1] < range1[0]:
        raise ValueError(f"Range1 is invalid: {range1}")

    if range2[1] < range2[0]:
        raise ValueError(f"Range2 is invalid: {range2}")

    is_overlapping = False

    if range2[0] >= range1[0] and range2[1] <= range1[1]:
        is_overlapping = True
    elif range1[0] >= range2[0] and range1[1] <= range2[1]:
        is_overlapping = True

    # print(f"range1: {range1}, range2: {range2} isOverlapping: {is_overlapping}")
    return is_overlapping


def are_ranges_overlapping_at_all(
    range1: Tuple[int, int], range2: Tuple[int, int]
) -> bool:
    if range1[1] < range1[0]:
        raise ValueError(f"Range1 is invalid: {range1}")

    if range2[1] < range2[0]:
        raise ValueError(f"Range2 is invalid: {range2}")

    is_overlapping = False

    if range2[0] >= range1[0] and range2[0] <= range1[1]:
        is_overlapping = True
    elif range1[0] >= range2[0] and range1[0] <= range2[1]:
        is_overlapping = True

    # print(f"range1: {range1}, range2: {range2} isOverlapping: {is_overlapping}")

    return is_overlapping


def part_1(data: Pairs) -> int:
    count = 0
    for pair in data:
        if are_ranges_overlapping(pair[0], pair[1]):
            count += 1
    return count


def part_2(data: Pairs) -> int:
    count = 0
    for pair in data:
        if are_ranges_overlapping_at_all(pair[0], pair[1]):
            count += 1
    return count


def main():
    pairs = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(pairs)
    assert part1_answer == 496
    print(f"Part I: {part1_answer} are the total of overlapping pairs")

    part2_answer = part_2(pairs)
    assert part2_answer == 847

    print(f"Part II: {part2_answer} are the total of overlapping pairs")


if __name__ == "__main__":
    main()
