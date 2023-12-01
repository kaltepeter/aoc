from copy import deepcopy
from functools import lru_cache, partial
from math import floor
import math
import os
from pathlib import Path
import re
from typing import Callable, List, Tuple, TypedDict
import numpy as np

base_path = Path(__file__).parent

# divisible by, true, false
MonkeyTest = Tuple[int, int, int]
Monkey = TypedDict(
    "Monkey",
    {
        "id": int,
        "starting_items": List[int],
        "operation": Callable[[str | int, str | int], int],
        "old_args": Tuple[str, ...],
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
            op_items = {"a": match_operation[0][0], "b": match_operation[0][2]}

            monkey = {
                "id": int(matchId[0]),
                "starting_items": starting_items,
                "operation": get_fn(match_operation[0]),
                "old_args": tuple(key for key, val in op_items.items() if val == "old"),
                "test": (
                    int(match_test[0][0]),
                    int(match_test[0][1]),
                    int(match_test[0][2]),
                ),
                "inspections": 0,
            }
            monkeys.append(monkey)

    return monkeys


def multiply(a: int, b: int) -> int:
    return np.multiply(a, b)


def add(a: int, b: int) -> int:
    return np.add(a, b)


def get_fn(op: Tuple[str, str, str]) -> Callable[[str | int, str | int], int]:
    left_item = int(op[0]) if op[0] != "old" else None
    right_item = int(op[2]) if op[2] != "old" else None
    match op[1]:
        case "*":
            return partial(multiply, a=left_item, b=right_item)
        case "+":
            return partial(add, a=left_item, b=right_item)
        case _:
            raise ValueError(f"Unknown instruction {op[1]}")


# def get_fn(old: int, op: str) -> int:
#     return eval(op)


# def get_fn(item: int, op: Tuple[str, str, str]) -> Callable[[str, str, str], int]:
#     left_item = item if op[0] == "old" else int(op[0])
#     right_item = item if op[2] == "old" else int(op[2])
#     match op[1]:
#         case "*":
#             return left_item * right_item
#         case "+":
#             return left_item + right_item
#         case _:
#             raise ValueError(f"Unknown instruction {op[1]}")


@lru_cache(maxsize=None)
def run_fn_with_args(
    item: int, op: Callable[[str | int, str | int], int], args: Tuple[str, ...]
) -> int:
    new = 0
    if ("a",) == args:
        new = op(a=item)
    elif ("b",) == args:
        new = op(b=item)
    elif (
        "a",
        "b",
    ) == args:
        new = op(a=item, b=item)
    else:
        raise ValueError(f"Unknown args {op['old_args']}")

    return new


def part_1(monkeys: List[Monkey]) -> int:
    # fns = {}
    for i in range(0, 20):
        for monkey in monkeys:
            for item in monkey["starting_items"]:
                new = 0
                op = monkey["operation"]
                new = run_fn_with_args(item, op, monkey["old_args"])
                new = worry_less(new)
                monkey_test = monkey["test"]
                next_monkey = (
                    monkey_test[1]
                    if np.mod(new, monkey_test[0]) == 0
                    else monkey_test[2]
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
    super_mod = math.prod([m["test"][0] for m in monkeys])
    for i in range(0, 10000):
        for monkey in monkeys:
            for item in monkey["starting_items"]:
                new = 0
                op = monkey["operation"]
                new = run_fn_with_args(item, op, monkey["old_args"])
                new = new % super_mod

                monkey_test = monkey["test"]
                next_monkey = (
                    monkey_test[1] if new % monkey_test[0] == 0 else monkey_test[2]
                )
                monkey["starting_items"] = monkey["starting_items"][1:]
                nm = monkeys[next_monkey]
                nm["starting_items"] = nm["starting_items"] + [new]
                monkeys[next_monkey] = nm
                monkey["inspections"] += 1

        # if (i) % 999 == 0 or i == 19:
        #     print(f"i: {i+1} monkeys: {[(m['id'], m['inspections']) for m in monkeys]}")

    top_two = sorted(monkeys, key=lambda monkey: monkey["inspections"], reverse=True)[
        :2
    ]
    return math.prod([m["inspections"] for m in top_two])


def main():
    monkeys = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(monkeys))
    print(f"Part I: {part1_answer} monkey business\n")
    assert part1_answer == 55458

    part2_answer = part_2(deepcopy(monkeys))
    print(f"Part II: {part2_answer} monkey business\n")
    assert part2_answer == 14508081294


if __name__ == "__main__":
    main()
