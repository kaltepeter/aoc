from copy import copy
from math import floor
import math
import os
from pathlib import Path
import re
from typing import Callable, List, Tuple, TypedDict

base_path = Path(__file__).parent

# divisible by, true, false
MonkeyTest = Tuple[int, int, int]
Monkey = TypedDict(
    "Monkey",
    {
        "id": int,
        "starting_items": List[int],
        "operation": Tuple[str, str, str],
        "test": MonkeyTest,
        "inspections": int,
    },
)


def worry_less(worry: int) -> int:
    return floor(worry / 3)


def process_input(file: str) -> List[Monkey]:
    monkeys = []
    with open(file) as reader:
        mList = reader.read().strip().split("\n\n")
        for m in mList:
            matchId = re.findall("Monkey (\\d+):", m)
            match_starting_items = re.findall("Starting items: ([\\d, ]+)", m)
            starting_items = [int(s) for s in match_starting_items[0].split(",")]
            match_operation = re.findall(
                "Operation: new = (.*) ([\\+\\-\\*\\/]) (.*)", m
            )
            match_test = re.findall(
                "Test: divisible by (\\d+)\\s+If true: throw to monkey (\\d+)\\s+If false: throw to monkey (\\d+)",
                m,
                re.MULTILINE,
            )

            monkey = {
                "id": int(matchId[0]),
                "starting_items": starting_items,
                "operation": match_operation[0],
                "test": (
                    int(match_test[0][0]),
                    int(match_test[0][1]),
                    int(match_test[0][2]),
                ),
                "inspections": 0,
            }
            monkeys.append(monkey)

    return monkeys


def get_fn(item: int, op: Tuple[str, str, str]) -> Callable[[str, str, str], int]:
    left_item = item if op[0] == "old" else int(op[0])
    right_item = item if op[2] == "old" else int(op[2])
    match op[1]:
        case "*":
            return left_item * right_item
        case "+":
            return left_item + right_item
        case _:
            raise ValueError(f"Unknown instruction {op[1]}")


def part_1(monkeys: List[Monkey]) -> int:
    fns = {}
    for i in range(0, 20):
        for monkey in monkeys:
            for item in monkey["starting_items"]:
                new = 0
                op = monkey["operation"]
                if not (item, op) in fns:
                    fns[(item, op)] = get_fn(item, op)

                new = fns[(item, op)]
                new = worry_less(new)
                monkey_test = monkey["test"]
                next_monkey = (
                    monkey_test[1] if new % monkey_test[0] == 0 else monkey_test[2]
                )
                monkey["starting_items"] = monkey["starting_items"][1:]
                nm = monkeys[next_monkey]
                nm["starting_items"] = nm["starting_items"] + [new]
                monkeys[next_monkey] = nm
                monkey["inspections"] += 1

                # print(
                #     f"item: {item} m.items: {monkey['starting_items']} m.inspections: {monkey['inspections']} new: {new} next_monkey: {next_monkey} nm.items: {nm['starting_items']}"
                # )

    top_two = sorted(monkeys, key=lambda monkey: monkey["inspections"], reverse=True)[
        :2
    ]
    return math.prod([m["inspections"] for m in top_two])


def part_2(monkeys: List[Monkey]) -> int:
    return 0


def main():
    monkeys = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(copy(monkeys))
    print(f"Part I: {part1_answer} monkey business\n")
    assert part1_answer == 55458

    part2_answer = part_2(copy(monkeys))
    print(f"Part II: {part2_answer} monkey business\n")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
