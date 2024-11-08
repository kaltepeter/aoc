from copy import deepcopy
import os
import re
from pathlib import Path
from typing import List
from functools import reduce

base_path = Path(__file__).parent

InputData = List[tuple[int, int]]


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        lists = []
        for line in reader.read().strip().split("\n"):
            lists.append(
                list(
                    map(
                        int,
                        list(
                            map(
                                lambda val: re.findall(r"\d+", val.strip()),
                                line.strip().splitlines(),
                            )
                        )[0],
                    )
                )
            )

        return list(zip(lists[0], lists[1]))


def process_input_part_2(file: str) -> tuple[int, int]:
    with open(file, "r") as reader:
        lists = []
        for line in reader.read().strip().split("\n"):
            lists.append(
                "".join(
                    list(
                        map(
                            lambda val: re.findall(r"\d+", val.strip()),
                            line.strip().splitlines(),
                        )
                    )[0]
                ),
            )

        return (int(lists[0]), int(lists[1]))


def part_1(data: InputData) -> int:
    race_combos = []
    for race in data:
        time, record = race
        speed = 0
        winners = []
        for i in range(1, time):
            speed = i * 1
            dist = (time - i) * speed
            if dist > record:
                winners.append(i)

        race_combos.append(len(winners))

    return reduce(lambda x, y: x * y, race_combos)


def part_2(race: tuple[int, int]) -> int:
    time, record = race
    winners = []

    def get_speed(x):
        return x * (time - x)

    lo = 0
    hi = time // 2
    if hi * (time - hi) < record:
        return 0
    assert get_speed(lo) < record and get_speed(hi) >= record
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if get_speed(mid) >= record:
            hi = mid
        else:
            lo = mid
    first = lo + 1
    assert get_speed(first) >= record and get_speed(first - 1) < record

    last = (time // 2) + (time // 2 - first) + (1 if time % 2 == 1 else 0)
    assert get_speed(last) >= record and get_speed(last + 1) < record

    # for i in range(1, time):
    #     speed = i * 1
    #     dist = (time - i) * speed
    #     if dist > record:
    #         winners.append(i)

    return last - first + 1


def main():
    pi = list(process_input(os.path.join(base_path, "input.txt")))
    pii = list(process_input_part_2(os.path.join(base_path, "input.txt")))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 500346

    part2_answer = part_2(deepcopy(pii))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 42515755


if __name__ == "__main__":
    main()
