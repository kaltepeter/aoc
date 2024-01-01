from copy import deepcopy
import os
from pathlib import Path
from typing import Generator, List


base_path = Path(__file__).parent

END = "OUT"
REJECTED = "R"
ACCEPTED = "A"
# ("a<2006", 'qkq)
Instruction = tuple[str, str]
# {'in': [('s<1351', 'px'), ('OUT', 'qqz)], 'gd': [('a>3333', 'R'), ('OUT', 'R')]}
Workflows = dict[str, List[Instruction]]
# {'x': 787, 'm': 2655, 'a': 1222, 's': 2876}
Part = dict[str, int]
InputData = tuple[Workflows, List[Part]]

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


def part_1(data: InputData) -> int:
    workflows, parts = data
    accepted_parts = []

    for part in parts:
        result = process_part(workflows, part)
        if result == ACCEPTED:
            accepted_parts.append(part)

    return calculate_ratings(accepted_parts)


def part_2(data: InputData) -> int:
    return 0


def main():
    pi = next(process_input(os.path.join(base_path, "input.txt")))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 446517

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
