from copy import deepcopy
from itertools import zip_longest
import os
from pathlib import Path
import re
from typing import Generator, List, Tuple

base_path = Path(__file__).parent

Packet = List[int | List[int]]
InputData = List[List[Packet]]


def safe_eval(pair: str) -> Packet:
    if not re.match(r"[\[\]\d\s,]+", pair):
        raise ValueError(f"Invalid input: {pair}")

    return eval(pair)


def process_input(file: str) -> Generator[InputData, None, None]:
    # packets = []
    with open(file, "r") as reader:
        for pairs in reader.read().split("\n\n"):
            yield list(map(safe_eval, pairs.splitlines()))
        # pairs = reader.read().strip().split("\n\n")
        # for p in pairs:
        #     pair = p.split("\n")
        #     if not re.match(r"[\[\]\d\s,]+", p):
        #         raise ValueError(f"Invalid input: {p}")

        #     packets.append((eval(pair[0]), eval(pair[1])))
    # return packets


def compare_ints(a: int, b: int) -> bool:
    return a <= b


def compare_pairs(
    left_list: Packet, right_list: Packet, results: List[bool] = list()
) -> Tuple[List[bool], Packet, Packet]:
    if isinstance(left_list, int) and isinstance(right_list, list):
        left_list = [left_list]
    elif isinstance(right_list, int) and isinstance(left_list, list):
        right_list = [right_list]

    while len(left_list) or len(right_list):
        print(f"lens: {len(left_list)} {left_list} {len(right_list)} {right_list}")
        if len(left_list) == 0:
            break

        if len(right_list) == 0:
            break

        left = left_list.pop(0)
        right = right_list.pop(0)

        if isinstance(left, int) and isinstance(right, int):
            val = left <= right
            print(f"left: {left} right: {right} results: {val}")
            results.append(val)
        else:
            print(f"break lists {type(left)} {type(left)} ")
            if isinstance(left, list) and isinstance(right, list):
                print(f"{len(left)} {len(right)}")
                if len(right) == 0 and len(left) > 0:
                    results.append(False)
                    return results, left_list, right_list

            compare_pairs(left, right, results)

    print(f"lists: {left_list} {right_list}")
    return results, left_list, right_list


# def process_pairs(left_list: Packet, right_list: Packet) -> Generator[bool, None, None]:
#     if isinstance(left_list, int) and isinstance(right_list, list):
#         left_list = [left_list]
#     elif isinstance(right_list, int) and isinstance(left_list, list):
#         right_list = [right_list]

#     while len(left_list) or len(right_list):
#         if len(left_list) == 0:
#             yield True
#             break

#         if len(right_list) == 0:
#             if len(left_list) >= 1:
#                 yield False
#                 return
#             break

#         left = left_list.pop(0)
#         right = right_list.pop(0)

#         if isinstance(left, int) and isinstance(right, int):
#             print(f"left: {left} right: {right} ")

#             if left < right:
#                 yield True
#                 return
#             elif left == right:
#                 yield True
#             else:
#                 yield False
#                 return

#         else:
#             yield from process_pairs(left, right)


def process_pairs(left_list: Packet, right_list: Packet) -> bool:
    for ll, rr in zip_longest(left_list, right_list, fillvalue=None):
        if ll == None:
            return True
        if rr == None:
            return False

        if isinstance(ll, int) and isinstance(rr, int):
            if ll > rr:
                return False
            if ll < rr:
                return True

        else:
            if isinstance(rr, int):
                rr = [rr]
            if isinstance(ll, int):
                ll = [ll]

            ret = process_pairs(ll, rr)
            if ret in [True, False]:
                return ret


def part_1(data: InputData) -> int:
    return sum([i for i, p in enumerate(data, 1) if process_pairs(*p) == True])


def part_2(data: InputData) -> int:
    return 0


def main():
    pi = list(process_input(os.path.join(base_path, "input.txt")))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} sum of pairs\n")
    assert part1_answer == 5623

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} sum of pairs\n")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
