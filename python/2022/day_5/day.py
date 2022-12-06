import copy
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple, TypedDict

base_path = Path(__file__).parent

Stack = List[str]
Stacks = Dict[int, Stack]
Move = Tuple[int, int, int]
Moves = List[Move]


def get_top_of_stacks(stacks: Stacks) -> str:
    top_of_stacks = ""
    for stack in stacks.values():
        top_of_stacks += stack[0]
    return top_of_stacks


def get_indexes_in_string(string: str, char: str) -> List[int]:
    return [i for i, ltr in enumerate(string) if ltr == char]


def process_input(file: str) -> Tuple[Stacks, Moves]:
    with open(file) as reader:
        stack_data, move_data = reader.read().split("\n\n")
        digit_data = {}  # {index: digit}
        valid_indexes = []
        stacks = {}

        for line in stack_data.split("\n"):
            matches_index_line = re.match("^[\\d\\s]+$", line)
            if matches_index_line:
                digits = re.finditer("\\d+", line)
                for digit in digits:
                    d = int(digit.group())
                    index_of_digit = line.index(str(d))
                    valid_indexes.append(index_of_digit)
                    stacks[d] = list()
                    digit_data[index_of_digit] = d

        for line in stack_data.split("\n"):
            found_chars = []
            chars_data = re.finditer("[A-Za-z]", line)
            chars = [char.group() for char in chars_data]

            for char in chars:
                if char in found_chars:
                    continue

                indexes_of_chars = get_indexes_in_string(line, char)
                index_match = set(indexes_of_chars).intersection(set(valid_indexes))

                if len(index_match) != len(indexes_of_chars):
                    raise (
                        ValueError(
                            f"Invalid index: {index_match} for valid {indexes_of_chars}"
                        )
                    )

                for char_index in indexes_of_chars:
                    stack_digit = digit_data[char_index]
                    stacks[stack_digit] = stacks[stack_digit] + [char]
                    # print(
                    #     f"stack_digit: {stack_digit} index_of_char: {char_index} char: {char}"
                    # )

                found_chars.append(char)

        get_moves = re.findall("move (\\d+) from (\\d+) to (\\d+)", move_data)
        moves = [(int(m[0]), int(m[1]), int(m[2])) for m in get_moves]

        return stacks, moves


def pretty_print_stacks(stacks: Stacks):
    for stack in stacks:
        print(f"stack: {stack} {stacks[stack]}")
    print()


def part_1(stacks: Stacks, moves: Moves) -> str:
    for move in moves:
        count, from_stack, to_stack = move
        # pretty_print_stacks(stacks)
        # print(f"Moving {count} from {from_stack} to {to_stack}")
        for i in range(count):
            item_to_move = stacks[from_stack][0]
            new_from_stack = stacks[from_stack][1:]
            stacks[to_stack].insert(0, item_to_move)
            stacks[from_stack] = new_from_stack

    return get_top_of_stacks(stacks)


def part_2(stacks: Stacks, moves: Moves) -> str:
    for move in moves:
        count, from_stack, to_stack = move

        items_to_move = stacks[from_stack][:count]
        new_from_stack = stacks[from_stack][count:]
        items_to_move.reverse()
        for i in items_to_move:
            stacks[to_stack].insert(0, i)

        stacks[from_stack] = new_from_stack

    return get_top_of_stacks(stacks)


def main():
    stacks, moves = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(copy.deepcopy(stacks), moves)
    print(f"Part I: {part1_answer} are the top boxes in order")
    assert part1_answer == "ZRLJGSCTR"

    part2_answer = part_2(copy.deepcopy(stacks), moves)
    print(f"Part II: {part2_answer} are the top boxes in order")
    assert part2_answer == "PRTTGRFPB"


if __name__ == "__main__":
    main()
