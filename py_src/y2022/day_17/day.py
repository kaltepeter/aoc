from copy import deepcopy
import itertools
import os
from pathlib import Path
from typing import Generator, List


base_path = Path(__file__).parent

CHAMBER_WIDTH = 7
InputData = str
# rocks = {
#     "dash": [0b0011110],
#     "plus": [0b0001000, 0b0011100, 0b0001000],
#     "elbow": [0b0011100, 0b0000100, 0b0000100],
#     "pipe": [0b0010000, 0b0010000, 0b0010000, 0b0010000],
#     "square": [
#         0b0011000,
#         0b0011000,
#     ],
# }
rocks = [
    [0, 1, 2, 3],
    [1, 1j, 1 + 1j, 2 + 1j, 1 + 2j],
    [0, 1, 2, 2 + 1j, 2 + 2j],
    [0, 1j, 2j, 3j],
    [0, 1, 1j, 1 + 1j],
]


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        return reader.read().splitlines()[0]


def print_tunnel_map(tunnel_map: List[int]) -> None:
    for row in reversed(tunnel_map):
        print(f"{row:0{CHAMBER_WIDTH}b}")


def get_bit(value, bit_index):
    return value & (1 << bit_index)


def get_normalized_bit(value, bit_index):
    return (value >> bit_index) & 1


def get_set_bit_indexes(value):
    return [i for i in range(CHAMBER_WIDTH) if get_normalized_bit(value, i)]


def get_highest_set_bit_index(value):
    return value.bit_length() - 1


def get_lowest_set_bit_index(value):
    return (value & -value).bit_length() - 1


def get_bit_size_for_rock(rock):
    index_map = {}
    for i in range(len(rock)):
        row = rock[i]
        index_map[i] = (
            get_lowest_set_bit_index(row),
            get_highest_set_bit_index(row),
        )

    return index_map


def modify_bit_range(number, position_start, position_end, operator):
    mask = 0
    orig_row = number
    for i in range(position_start, position_end + 1):
        if operator == 1:
            mask += 1 << i + operator
            orig_row += 1 << i
        elif operator == -1:
            print(i, operator)
            if i > 0:
                mask += 1 >> (i + operator)
            else:
                mask += 1 >> 0
            orig_row += 1 >> i

    # orig_row = number & ~mask
    print(f"mask: {mask:07b} orig_row: {orig_row:07b} result: {(orig_row | mask):07b}")
    return orig_row | mask


def shift_masked(value: int, mask: int, operator) -> int:
    masked_value = value & mask
    shifted = None
    if operator == 1:
        shifted = masked_value >> 1
    else:
        shifted = masked_value << 1
    return (value & ~mask) | shifted


def simulate_tower(data: InputData, num_rocks: int) -> int:
    jets = [1 if x == ">" else -1 for x in data]
    solid = {x - 1j for x in range(7)}
    height = 0

    rock_count = 0
    rock_index = 0
    rock = {x + 2 + (height + 3) * 1j for x in rocks[rock_index]}

    while rock_count < num_rocks:
        for jet in jets:
            moved = {x + jet for x in rock}
            if all(0 <= x.real < 7 for x in moved) and not (moved & solid):
                rock = moved
            moved = {x - 1j for x in rock}
            if moved & solid:
                solid |= rock
                rock_count += 1
                height = max(x.imag for x in solid) + 1
                if rock_count >= num_rocks:
                    break
                rock_index = (rock_index + 1) % 5
                rock = {x + 2 + (height + 3) * 1j for x in rocks[rock_index]}
            else:
                rock = moved

    return int(height)


def summarize(solid: set[complex]):
        o = [-20] * CHAMBER_WIDTH

        for x in solid:
            r = int(x.real)
            i = int(x.imag)
            o[r] = max(o[r], i)

        top = max(o)
        return tuple(x - top for x in o)


def simulate_tower_ii(data: InputData, T: int) -> int:
    jets = [1 if x == ">" else -1 for x in data]
    solid = {x - 1j for x in range(CHAMBER_WIDTH)}
    height = 0

    seen = {}

    rock_count = 0

    rock_index = 0
    rock = {x + 2 + (height + 3) * 1j for x in rocks[rock_index]}

    while rock_count < T:
        for ji, jet in enumerate(jets):
            moved = {x + jet for x in rock}
            if all(0 <= x.real < CHAMBER_WIDTH for x in moved) and not (moved & solid):
                rock = moved
            moved = {x - 1j for x in rock}
            if moved & solid:
                solid |= rock
                rock_count += 1
                o = height
                height = max(x.imag for x in solid) + 1

                if rock_count >= T:
                    break

                rock_index = (rock_index + 1) % 5
                rock = {x + 2 + (height + 3) * 1j for x in rocks[rock_index]}
                key = (ji, rock_index, summarize(solid))
                if key in seen:
                    lrc, lh = seen[key]
                    rem = T - rock_count
                    rep = rem // (rock_count - lrc)
                    offset = rep * (height - lh)
                    rock_count += rep * (rock_count - lrc)
                    seen = {}
                seen[key] = (rock_count, height)
            else:
                rock = moved

    return int(height + offset)


def part_1(data: InputData) -> int:
    return simulate_tower(data, 2022)


# def part_1(data: InputData) -> int:
#     max_rocks = 10
#     tunnel_map = [0b0000000, 0b0000000, 0b0000000]
#     jets, jets_backup = itertools.tee(data)

#     fallen_rocks: int = 0
#     for r in itertools.cycle(rocks.keys()):
#         if fallen_rocks > max_rocks:
#             break

#         landed = False

#         start, end = len(tunnel_map), len(rocks[r])
#         tunnel_map += rocks[r]
#         rock_indexes = get_bit_size_for_rock(rocks[r])
#         print(f"fallen_rocks: {fallen_rocks} rock: {r} ri: {rock_indexes}")
#         print_tunnel_map(tunnel_map)
#         print("")

#         for move in itertools.cycle(("J", "D")):
#             print(f"move: {move} landed: {landed} start: {start} end: {end}")
#             if landed == True:
#                 fallen_rocks += 1
#                 break

#             if move == "D":
#                 if start == 0 or (tunnel_map[start - 1] & tunnel_map[start]) != 0:
#                     landed = True
#                 else:
#                     # head, rock, tail = (
#                     #     tunnel_map[: start - 1],
#                     #     tunnel_map[start : start + end],
#                     #     tunnel_map[start - 1 : start] + tunnel_map[start + end :],
#                     # )
#                     # print(head, rock, tail)
#                     # tunnel_map = head + rock + tail
#                     max_height = 0
#                     for i in range(start, start + end):
#                         if start != 0:
#                             # if tunnel_map[i] & tunnel_map[i + 1]:
#                             #     print("would collide")
#                             #     next

#                             print(f"down bits {tunnel_map[i]:07b}")
#                             tunnel_map[i - 1] |= tunnel_map[i]
#                             tunnel_map[i] = 0b0000000
#                         else:
#                             raise Exception(f"start equal zero")
#                         max_height = i

#                     start, end = start - 1, start + end - start
#                     tunnel_map = tunnel_map[: max_height + 3]

#             if move == "J":
#                 try:
#                     jet = next(jets)
#                 except StopIteration:
#                     jets, jets_backup = itertools.tee(jets_backup)
#                     jet = next(jets)

#                 temp_tunnel_map = {}
#                 print(f"jet: {jet} start: {start} end: {end}")
#                 for i in range(start, start + end):
#                     current_rock_index = i - start
#                     # TODO: need to track current rock indexes, to identify current rock vs existing
#                     # the rock shifts because i don't know current from existing
#                     will_hit_wall_or_rock = False
#                     set_bits = get_set_bit_indexes(tunnel_map[i])
#                     print(f"set_bits: {set_bits} tunnel_map[i]: {tunnel_map[i]:07b}")
#                     print(f"before: {rock_indexes} {current_rock_index} {start}")
#                     match jet:
#                         case ">":
#                             compare_bit = rock_indexes[current_rock_index][0] - 1
#                             print(f"compare_bit: {compare_bit}")
#                             if compare_bit >= 0 and not get_normalized_bit(
#                                 tunnel_map[i], compare_bit
#                             ):
#                                 temp_tunnel_map[i] = tunnel_map[i] >> 1
#                                 rock_indexes[current_rock_index] = (
#                                     rock_indexes[current_rock_index][0] - 1,
#                                     rock_indexes[current_rock_index][1] - 1,
#                                 )
#                             else:
#                                 will_hit_wall_or_rock = True
#                                 print(f"will_hit_wall_or_rock: {will_hit_wall_or_rock}")
#                                 break
#                         case "<":
#                             compare_bit = rock_indexes[current_rock_index][1] + 1
#                             print(f"compare_bit: {compare_bit}")
#                             if compare_bit < CHAMBER_WIDTH and not get_normalized_bit(
#                                 tunnel_map[i], compare_bit
#                             ):
#                                 temp_tunnel_map[i] = tunnel_map[i] << 1
#                                 rock_indexes[current_rock_index] = (
#                                     rock_indexes[current_rock_index][0] + 1,
#                                     rock_indexes[current_rock_index][1] + 1,
#                                 )
#                             else:
#                                 will_hit_wall_or_rock = True
#                                 print(f"will_hit_wall_or_rock: {will_hit_wall_or_rock}")
#                                 break
#                         case _:
#                             raise Exception("Invalid jet direction")

#                 if not will_hit_wall_or_rock:
#                     for i, v in temp_tunnel_map.items():
#                         tunnel_map[i] = v

#                 print(f"after: {rock_indexes}")
#             print_tunnel_map(tunnel_map)
#             # print("")

#     # only shift rock bits
#     return len(tunnel_map)


def part_2(data: InputData) -> int:
    return simulate_tower_ii(data, 1000000000000)


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 3209

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 1580758017509


if __name__ == "__main__":
    main()
