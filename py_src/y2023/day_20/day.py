from copy import deepcopy
import os
from pathlib import Path
from typing import Generator, List, Deque
from queue import PriorityQueue, deque

base_path = Path(__file__).parent

InputData = dict[str, tuple[str, List[str]]]
LOW = 0
HIGH = 1
OFF = 0
ON = 1
FLIP_FLOP = "%"
CONJUNCTION = "&"
BROADCAST = "b"


class Module:
    def __init__(self, name: str, module_type: str, outputs: List[str]):
        self.name = name
        self.module_type = module_type
        self.outputs = outputs

        if module_type == FLIP_FLOP:
            self.memory = OFF
        else:
            self.memory = {}

    def __repr__(self) -> str:
        return f"{self.name}{{module_type={self.module_type}, outputs={','.join(self.outputs)}, memory={str(self.memory)}}}"


# {'broadcaster': Module}
State = dict[str, Module]
Pulses = tuple[int, int]
# ('', 'broadcaster', LOW) or (input, output, value)
QueueItem = tuple[str, str, int]


def process_input(file: str) -> Generator[InputData, None, None]:
    with open(file, "r") as reader:
        for blocks in reader.read().split("\n\n"):
            res = list(map(lambda val: val.strip().split(" -> "), blocks.splitlines()))
            yield {
                item[0]
                .replace(FLIP_FLOP, "")
                .replace(CONJUNCTION, ""): (item[0][:1], item[1].split(", "))
                for item in res
            }


def push_button(
    state: State,
    q: Deque[QueueItem],
) -> Pulses:
    lo = 0
    hi = 0

    while q:
        item = q.popleft()
        input_name, name, pulse = item

        if pulse == LOW:
            lo += 1
        else:
            hi += 1

        if not state.get(name, False):
            continue

        module = state[name]

        if module.module_type == FLIP_FLOP:
            if pulse == LOW:
                module.memory ^= 0b1
                for output in module.outputs:
                    q.append((module.name, output, module.memory))

        else:
            module.memory[input_name] = pulse
            # value = (value << 1) | 1
            value = LOW if all(x == HIGH for x in module.memory.values()) else HIGH
            for output in module.outputs:
                q.append((module.name, output, value))

    return (lo, hi)


def part_1(data: InputData) -> int:
    button_pushes = 1000
    state: State = {}

    for name, (module, outputs) in data.items():
        if name == "broadcaster":
            continue

        state[name] = Module(name, module, outputs)

    for name, module in state.items():
        for output in module.outputs:
            if output in state and state.get(output).module_type == CONJUNCTION:
                state[output].memory[name] = LOW

    # low, high
    lo = 0
    hi = 0
    for _ in range(button_pushes):
        lo += 1
        q: Deque[QueueItem] = deque(
            [("broadcaster", output, LOW) for output in data["broadcaster"][1]]
        )
        pc = push_button(state, q)
        lo += pc[0]
        hi += pc[1]

    return (lo) * (hi)


def part_2(data: InputData) -> int:
    return 0


def main():
    pi = next(process_input(os.path.join(base_path, "input.txt")))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 731517480

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
