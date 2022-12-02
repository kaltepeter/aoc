import os
from pathlib import Path
from typing import List, TypedDict

base_path = Path(__file__).parent

Elf = TypedDict("Elf", {"items": List[int], "calories": int})
Elves = List[Elf]


def calc_calories(elf: Elf) -> int:
    return sum(elf["items"])


def process_input(file: str) -> Elves:
    with open(file) as reader:
        elf_data = reader.read().strip().split("\n\n")
        elf_list = [e.split("\n") for e in elf_data]
        return [{"items": [int(e) for e in elf]} for elf in elf_list]


def part_1(elves: Elves) -> int:
    return max([calc_calories(elf) for elf in elves])


def part_2(elves: Elves) -> int:
    for elf in elves:
        elf["calories"] = calc_calories(elf)
    top_three = sorted(elves, key=lambda elf: elf["calories"], reverse=True)[:3]
    return sum(d["calories"] for d in top_three)


def main():
    elves = process_input(os.path.join(base_path, "input.txt"))

    print(f"Part I: {part_1(elves)} is the most calories")

    print(
        f"Part II: {part_2(elves)} is the sum of the top three highest calorie counts"
    )


if __name__ == "__main__":
    main()
