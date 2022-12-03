import os
from pathlib import Path
import string
from typing import Dict, List, Set, Tuple, TypedDict


base_path = Path(__file__).parent

lower_letters = string.ascii_lowercase[:26]
upper_letters = string.ascii_uppercase[:26]
priorities = [i for i in range(1, 52 + 1)]
letters = lower_letters + upper_letters

Rucksack = TypedDict(
    "Rucksack", {"compartment_1": str, "compartment_2": str, "common_items": List[str]}
)
Rucksacks = List[Rucksack]

ElfGroup = Tuple[str, str, str]
Groups = List[ElfGroup]


def split_word_in_half(word: str) -> List[str]:
    if len(word) % 2 != 0:
        raise ValueError("Word must be even length")
    half = len(word) // 2
    return (word[:half], word[half:])


def find_common_items(items: Tuple[str, ...]) -> Set[str]:
    return set(items[0]).intersection(*items[1:])
    # return set([item for item in items[0] if item in items[1]])


def calc_priority(item: str) -> int:
    return priorities[letters.index(item)]


def process_input(file: str) -> Rucksacks:
    with open(file) as reader:
        data = reader.read().strip().split("\n")
        items = [split_word_in_half(rucksack) for rucksack in data]
        return [
            {
                "compartment_1": item[0],
                "compartment_2": item[1],
                "common_items": find_common_items(item),
            }
            for item in items
        ]


def process_groups_input(file: str) -> Groups:
    with open(file) as reader:
        data = reader.read().strip().split("\n")
        return [tuple(data[i : i + 3]) for i in range(0, len(data), 3)]


def part_1(data: Rucksacks) -> int:
    return sum(
        [
            sum([calc_priority(item) for item in rucksack["common_items"]])
            for rucksack in data
        ]
    )


def part_2(data: Groups) -> int:
    common_items = [find_common_items(item) for item in data]
    return sum([sum([calc_priority(item) for item in items]) for items in common_items])


def main():
    rucksacks = process_input(os.path.join(base_path, "input.txt"))
    groups = process_groups_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(rucksacks)
    assert part1_answer == 7428
    print(f"Part I: {part1_answer} is the total of the priorities")

    part2_answer = part_2(groups)
    assert part2_answer == 2650

    print(f"Part II: {part2_answer} is the total of the priorities")


if __name__ == "__main__":
    main()
