from copy import deepcopy
import os
from pathlib import Path
from typing import List, Tuple

from py_src.shared.graph import Location, WeightedGraph


base_path = Path(__file__).parent

Coord = Tuple[int, int]
HeightMap = type(WeightedGraph[Location, float])
MAX_HEIGHT_DIFF = 1


def process_input(file: str) -> List[str]:
    return []


def part_1(data: List[str]) -> int:
    return 0


def part_2(data: List[str]) -> int:
    return 0


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} monkey business\n")
    assert part1_answer == 0

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} monkey business\n")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
