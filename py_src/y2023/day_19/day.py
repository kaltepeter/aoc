from copy import deepcopy
import os
from pathlib import Path
from typing import Generator, List
import re

base_path = Path(__file__).parent

END = "OUT"
REJECTED = "R"
ACCEPTED = "A"
# ("a<2006", 'qkq)
Instruction = tuple[str, str]
# {'in': [('s<1351', 'px'), ('OUT', 'qqz)], 'gd': [('a>3333', 'R'), ('OUT', 'R')]}
Workflows = dict[str, List[Instruction]]
Workflow = tuple[str, List[Instruction]]
# {'x': 787, 'm': 2655, 'a': 1222, 's': 2876}
Part = dict[str, int]
InputData = tuple[Workflows, List[Part]]
RPart = dict[str, tuple[int, int]]
WorkflowMap = dict[str, tuple[List[tuple[str, str, int, str]], str]]

final_states = [REJECTED, ACCEPTED]


def process_input(file: str) -> Generator[InputData, None, None]:
    with open(file, "r") as reader:
        blocks = reader.read().split("\n\n")
        workflow_input, parts = blocks

        workflow_input = [
            line.replace("}", "").split("{") for line in workflow_input.splitlines()
        ]

        workflows = {}
        for key, val in workflow_input:
            workflows[key]: List[Instruction] = []
            for ins in (v.split(":") for v in val.split(",")):
                steps, out = ins if len(ins) > 1 else (END, ins[0])
                workflows[key].append((steps, out))

        parts = [
            {k: int(v) for k, v in (x.split("=") for x in p.split(","))}
            for p in (
                part.strip().replace("{", "").replace("}", "")
                for part in parts.splitlines()
            )
        ]

        yield (workflows, parts)


def process_input_part_2(
    file: str,
) -> WorkflowMap:
    block, _ = open(file).read().split("\n\n")

    workflows: WorkflowMap = {}

    for line in block.splitlines():
        name, rest = line[:-1].split("{")
        rules = rest.split(",")
        workflows[name] = ([], rules.pop())
        for rule in rules:
            comparison, target = rule.split(":")
            key = comparison[0]
            cmp = comparison[1]
            n = int(comparison[2:])
            workflows[name][0].append((key, cmp, n, target))

    return workflows


def calculate_ratings(accepted_parts: List[Part]) -> int:
    return sum(sum(part.values()) for part in accepted_parts)


def process_part(
    workflows: Workflows, part: Part, workflow: str = "in", step_count: int = 0
) -> str:
    result = None

    step, success = workflows[workflow][step_count]

    if step == END and success in final_states:
        return success

    while result == None:
        exp = eval(step, {}, {**part, END: success})

        if exp:
            if success in final_states:
                return success

            result = process_part(workflows, part, success, 0)
        else:
            result = process_part(workflows, part, workflow, step_count + 1)

    return result


def count(workflows: Workflows, ranges: dict[str, tuple[int, int]], id="in"):
    if id == REJECTED:
        return 0

    if id == ACCEPTED:
        product = 1
        for lo, hi in ranges.values():
            product *= hi - lo + 1
        return product

    rules, fallback = workflows[id]

    total = 0
    for key, cmp, n, target in rules:
        lo, hi = ranges[key]
        if cmp == "<":
            T = (lo, min(n - 1, hi))
            F = (max(n, lo), hi)
        else:
            T = (max(n + 1, lo), hi)
            F = (lo, min(n, hi))

        if T[0] <= T[1]:
            copy = dict(ranges)
            copy[key] = T
            total += count(workflows, copy, target)

        if F[0] <= F[1]:
            ranges = dict(ranges)
            ranges[key] = F
        else:
            break

    else:
        total += count(workflows, ranges, fallback)

    return total


def part_1(data: InputData) -> int:
    workflows, parts = data
    accepted_parts = []

    for part in parts:
        result = process_part(workflows, part)
        if result == ACCEPTED:
            accepted_parts.append(part)

    return calculate_ratings(accepted_parts)


def part_2(data: WorkflowMap) -> int:
    result = count(data, {key: (1, 4000) for key in "xmas"})

    return result


def main():
    in_file = os.path.join(base_path, "input.txt")
    pi = next(process_input(in_file))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 446517

    part2_answer = part_2(process_input_part_2(in_file))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 130090458884662


if __name__ == "__main__":
    main()
