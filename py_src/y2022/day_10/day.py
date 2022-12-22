from copy import copy
import os
from pathlib import Path
from typing import List, Literal
from PIL import Image

base_path = Path(__file__).parent

Func = Literal["noop", "addx"]
Instructions = List[tuple[Func, int]]
# since the question is about 'during', its previous cycle
interesting_cycles = (19, 59, 99, 139, 179, 219)


def process_input(file: str) -> Instructions:
    with open(file) as reader:
        lines = reader.read().strip().split("\n")
        inst = [line.strip().split(" ") for line in lines]
        return [
            (
                i[0],
                int(i[1]) if len(i) > 1 else 0,
            )
            for i in inst
        ]


# def get_interesting_cycles(state: dict[int, int]) -> List[int]:
#     highest_key = sorted(state.keys())[-1]
#     return [i for i in range(20, highest_key + 1, 40)]


def get_signal_strength(state: dict[int, int]) -> int:
    values = [(v[0] + 1) * v[1] for v in state.items() if v[0] in interesting_cycles]
    return sum(values)


def get_state(instructions: Instructions) -> dict[int, int]:
    state = {}
    cycles_to_run = {}
    inst = None
    for idx in range(1, 240):
        cycle = idx

        # init register
        register = state[cycle - 1] if cycle - 1 in state else 1
        state[cycle] = register

        # print(
        #     f"cycle: {cycle} ({inst}, {register}) cycles_to_run: {cycles_to_run} inst_left: {len(instructions)}"
        # )

        if cycle in cycles_to_run:
            register += cycles_to_run[cycle]
            del cycles_to_run[cycle]
            state[cycle] = register
            continue

        if len(instructions) > 0:
            inst = instructions.pop(0)

            match inst[0]:
                case "noop":
                    continue
                case "addx":
                    cycles_to_run[cycle + 1] = inst[1]
                case _:
                    raise ValueError(f"Unknown instruction {inst[0]}")

    return state


def part_1(instructions: Instructions) -> int:
    state = get_state(instructions)

    # print(state)
    # for c in interesting_cycles:
    #     print(f"{c}: {state[c]}")

    return get_signal_strength(state)


def part_2(instructions: Instructions) -> str:
    state = get_state(instructions)
    # vals = set(state.values())
    # print(vals)
    out = ""
    for i in range(0, 240):
        register = state[i] if i in state else 0
        # print(f"register: {register} i: {i}")

        rowI = i % 40

        if rowI == 0:
            out += "\n"

        if rowI in range(register - 1, register + 2):
            out += "#"
            # out += "█"
        else:
            out += "."
            # out += " "

    print(out.strip())
    return out.strip()


def main():
    instructions = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(copy(instructions))
    print(f"Part I: {part1_answer} signal strength\n")
    assert part1_answer == 16880

    part2_answer = part_2(copy(instructions))
    print(f"Part II: {len(part2_answer)} length of chars\n")
    assert len(part2_answer) == 245


if __name__ == "__main__":
    main()
