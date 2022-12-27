from copy import deepcopy
from functools import cmp_to_key
from itertools import chain, zip_longest
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


def compare(left_list: Packet, right_list: Packet) -> int:
    for ll, rr in zip_longest(left_list, right_list, fillvalue=None):
        if ll == None:
            return 1
        if rr == None:
            return -1
            return True
        if rr == None:
            return False

        if isinstance(ll, int) and isinstance(rr, int):
            if ll > rr:
                return -1
            if ll < rr:
                return 1
                return True

        else:
            if isinstance(rr, int):
                rr = [rr]
            if isinstance(ll, int):
                ll = [ll]

            ret = compare(ll, rr)
            if ret in [1, -1]:
            ret = process_pairs(ll, rr)
            if ret in [True, False]:
                return ret


def part_1(data: InputData) -> int:
    return sum([i for i, p in enumerate(data, 1) if compare(*p) == 1])


def part_2(data: InputData) -> int:
    div1, div2 = [[2]], [[6]]
    all_packets = list(
        chain(*[ele if isinstance(ele, list) else [ele] for ele in data])
    ) + [div1, div2]

    sorted_packets = sorted(all_packets, key=cmp_to_key(compare), reverse=True)
    return (sorted_packets.index(div1) + 1) * (sorted_packets.index(div2) + 1)


def main():
    pi = list(process_input(os.path.join(base_path, "input.txt")))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} sum of pairs\n")
    assert part1_answer == 5623

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} decoder key\n")
    assert part2_answer == 20570


if __name__ == "__main__":
    main()
