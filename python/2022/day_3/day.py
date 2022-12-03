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


def split_word_in_half(word: str) -> List[str]:
    if len(word) % 2 != 0:
        raise ValueError("Word must be even length")
    half = len(word) // 2
    return (word[:half], word[half:])


def find_common_items(items: Tuple[str, str]) -> Set[str]:
    return set([item for item in items[0] if item in items[1]])


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


def part_1(data: Rucksacks) -> int:
    return sum(
        [
            sum([calc_priority(item) for item in rucksack["common_items"]])
            for rucksack in data
        ]
    )


def part_2(data: Rucksacks) -> int:
    return 0


def main():
    game = process_input(os.path.join(base_path, "input.txt"))

    print(f"Part I: {part_1(game)} is the total of the priorities")

    print(f"Part II: {part_2(game)} is the total of the priorities")


if __name__ == "__main__":
    main()
