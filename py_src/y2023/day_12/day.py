from copy import deepcopy
import os
from pathlib import Path
from typing import Generator, List
import re

base_path = Path(__file__).parent


UNKNOWN = "?"
DAMAGED = "#"
OPERATIONAL = "."

Row = tuple[str, List[int]]
InputData = List[Row]
Record = tuple[str, tuple[int]]


def process_input(file: str) -> Generator[InputData, None, None]:
    with open(file, "r") as reader:
        for m in reader.read().split("\n\n"):
            r = []
            for row in m.splitlines():
                spring_report, count_report = row.split(" ")
                # damaged = list(re.finditer(r"([\?#])+", spring_report))
                counts = [int(count) for count in count_report.split(",")]
                r.append((spring_report, counts))

            yield r


cache = {}


def find_broken_springs(rec: Record) -> int:
    arrangement, counts = rec
    if arrangement == "":
        return 1 if counts == () else 0
    if counts == ():
        return 0 if DAMAGED in arrangement else 1

    key = (arrangement, counts)
    if key in cache:
        return cache[key]
    result = 0

    if arrangement[0] in [OPERATIONAL, UNKNOWN]:
        result += find_broken_springs((arrangement[1:], counts))

    if arrangement[0] in [DAMAGED, UNKNOWN]:
        if (
            counts[0] <= len(arrangement)
            and OPERATIONAL not in arrangement[: counts[0]]
            and (counts[0] == len(arrangement) or arrangement[counts[0]] != DAMAGED)
        ):
            result += find_broken_springs((arrangement[counts[0] + 1 :], counts[1:]))

    cache[key] = result
    return result


def unfold(rec: Record) -> Record:
    arrangement, counts = rec
    moar = ((arrangement + UNKNOWN) * 5)[:-1]
    count_list = list(counts) * 5

    return (moar, tuple(count_list))


def part_1(data: InputData) -> int:
    total = 0
    for matches, counts in data:
        total += find_broken_springs((matches, tuple(counts)))

    return total


def part_2(data: InputData) -> int:
    total = 0
    for row in data:
        matches, counts = unfold(row)
        total += find_broken_springs((matches, tuple(counts)))

    return total


def main():
    pi = list(process_input(os.path.join(base_path, "input.txt")))

    part1_answer = part_1(deepcopy(pi)[0])
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 7916

    part2_answer = part_2(deepcopy(pi)[0])
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 37366887898686


if __name__ == "__main__":
    main()
