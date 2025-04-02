from collections import deque
from copy import deepcopy
from functools import lru_cache
from itertools import combinations, permutations, product
import os
from pathlib import Path
from typing import Generator, List, Optional


base_path = Path(__file__).parent

Coord = tuple[int, int]
InputData = List[str]


numeric_keypad = {
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "0": (1, 3),
    "A": (2, 3),
}

directional_keypad = {
    "^": (1, 0),
    "A": (2, 0),
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1),
}

dirctions = {
    ">": (1, 0),
    "<": (-1, 0),
    "^": (0, -1),
    "v": (0, 1),
}

def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        block = reader.read().split("\n\n")[0]
        return block.splitlines()


def calc_complexity(code: str, sequence_length: int) -> int:
    return sequence_length * int(code.replace("A", ""))


def get_combos(char_a, a, char_b, b) -> Generator[str, None, None]:
    for idxs in combinations(range(a + b), r=a):
        res = [char_b] * (a + b)
        for i in idxs:
            res[i] = char_a
        yield "".join(res)


@lru_cache(None)
def find_paths(code: str, number_pad: bool) -> str:
    keypad = numeric_keypad if number_pad else directional_keypad

    parts = []
    current_pos = keypad["A"]

    for char in code:
        next_location = keypad[char]
        dx = next_location[0] - current_pos[0]
        dy = next_location[1] - current_pos[1]

        moves = []
        if dx > 0:
            moves += [">", dx]
        else:
            moves += [ "<", -dx]
        
        if dy > 0:
            moves += ["v", dy]
        else:
            moves += ["^", -dy]

        perms = list(set(["".join(x) + "A" for x in get_combos(*moves)]))
        combos = []
        for combo in perms:
            cx, cy = current_pos
            good = True
            for c in combo[:-1]:
                dx, dy = dirctions[c]
                cx, cy = cx + dx, cy + dy
                if not (cx, cy) in keypad.values():
                    good = False
                    break
            if good:
                combos.append(combo)

        parts.append(combos)
        current_pos = next_location

    return ["".join(x) for x in product(*parts)]


@lru_cache(None)
def find_paths_2(a: str, b: str, keypad: bool) -> str:
    keypad = directional_keypad if keypad else numeric_keypad

    current_pos = keypad[a]
    next_pos = keypad[b]
    dx = next_pos[0] - current_pos[0]
    dy = next_pos[1] - current_pos[1]

    moves = []
    if dx > 0:
        moves += [">", dx]
    else:
        moves += [ "<", -dx]
    
    if dy > 0:
        moves += ["v", dy]
    else:
        moves += ["^", -dy]

    perms = list(set(["".join(x) + "A" for x in get_combos(*moves)]))
    combos = []
    for combo in perms:
        cx, cy = current_pos
        good = True
        for c in combo[:-1]:
            dx, dy = dirctions[c]
            cx, cy = cx + dx, cy + dy
            if not (cx, cy) in keypad.values():
                good = False
                break
        if good:
            combos.append(combo)

    return combos


@lru_cache(None)
def get_cost(a: str, b: str, keypad: bool, depth: int = 0) -> int:
    if depth == 0:
        assert keypad
        return min([len(x) for x in find_paths_2(a, b, True)])
    
    paths = find_paths_2(a, b, keypad)
    base_cost = 1<<60
    for seq in paths:
        seq = "A" + seq
        cost = 0
        for i in range(len(seq) - 1):
            a, b = seq[i], seq[i + 1]
            cost += get_cost(a, b, True, depth - 1)

        base_cost = min(base_cost, cost)

    return base_cost


def get_code_cost(code: str, depth: int) -> int:
    code = "A" + code
    cost = 0
    for i in range(len(code) - 1):
        a, b = code[i], code[i + 1]
        cost += get_cost(a, b, False, depth)

    return cost


def part_1(data: InputData) -> int:
    result = 0
    for code in data:
        result += get_code_cost(code, 2) * int(code[:-1])

    return result


def part_2(data: InputData) -> int:
    result = 0
    for code in data:
        result += get_code_cost(code, 25) * int(code[:-1])

    return result


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 219366

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 271631192020464


if __name__ == "__main__":
    main()
