from copy import deepcopy
import itertools
import os
from pathlib import Path
from typing import Generator, List


base_path = Path(__file__).parent

CHAMBER_WIDTH = 7
InputData = Generator[str, None, None]
rocks = {
    "dash": [0b0011110],
    "plus": [0b0001000, 0b0011100, 0b0001000],
    "elbow": [0b0011100, 0b0000100, 0b0000100],
    "pipe": [0b0010000, 0b0010000, 0b0010000, 0b0010000],
    "square": [
        0b0011000,
        0b0011000,
    ],
}


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        for line in reader.read():
            for char in line.split():
                yield char


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


def part_1(data: InputData) -> int:
    max_rocks = 10
    tunnel_map = [0b0000000, 0b0000000, 0b0000000]
    jets, jets_backup = itertools.tee(data)

    fallen_rocks: int = 0
    for r in itertools.cycle(rocks.keys()):
        if fallen_rocks > max_rocks:
            break

        landed = False

        start, end = len(tunnel_map), len(rocks[r])
        tunnel_map += rocks[r]
        x_end, x_start = 0, 0
        rock_indexes = get_bit_size_for_rock(rocks[r])
        print(f"fallen_rocks: {fallen_rocks} rock: {r} ri: {rock_indexes}")
        print_tunnel_map(tunnel_map)
        print("")

        for move in itertools.cycle(("J", "D")):
            print(f"move: {move} landed: {landed} start: {start} end: {end}")
            if landed == True:
                fallen_rocks += 1
                break

            if move == "D":
                if start == 0 or (tunnel_map[start - 1] & tunnel_map[start]) != 0:
                    landed = True
                else:
                    # head, rock, tail = (
                    #     tunnel_map[: start - 1],
                    #     tunnel_map[start : start + end],
                    #     tunnel_map[start - 1 : start] + tunnel_map[start + end :],
                    # )
                    # print(head, rock, tail)
                    # tunnel_map = head + rock + tail
                    max_height = 0
                    for i in range(start, start + end):
                        if start != 0:
                            tunnel_map[i - 1] |= tunnel_map[i]
                            tunnel_map[i] = 0b0000000
                        else:
                            raise Exception(f"start equal zero")
                        max_height = i

                    start, end = start - 1, start + end - start
                    tunnel_map = tunnel_map[: max_height + 3]

            if move == "J":
                try:
                    jet = next(jets)
                except StopIteration:
                    jets, jets_backup = itertools.tee(jets_backup)
                    jet = next(jets)

                temp_tunnel_map = {}
                print(f"jet: {jet} start: {start} end: {end}")
                for i in range(start, start + end):
                    current_rock_index = i - start
                    # TODO: need to track current rock indexes, to identify current rock vs existing
                    # the rock shifts because i don't know current from existing
                    will_hit_wall_or_rock = False
                    set_bits = get_set_bit_indexes(tunnel_map[i])
                    print(f"set_bits: {set_bits} tunnel_map[i]: {tunnel_map[i]:07b}")
                    print(f"before: {rock_indexes} {current_rock_index} {start}")
                    match jet:
                        case ">":
                            compare_bit = rock_indexes[current_rock_index][0] - 1
                            print(f"compare_bit: {compare_bit}")
                            if compare_bit >= 0 and not get_normalized_bit(
                                tunnel_map[i], compare_bit
                            ):
                                temp_tunnel_map[i] = tunnel_map[i] >> 1
                                rock_indexes[current_rock_index] = (
                                    rock_indexes[current_rock_index][0] - 1,
                                    rock_indexes[current_rock_index][1] - 1,
                                )
                            else:
                                will_hit_wall_or_rock = True
                                print(f"will_hit_wall_or_rock: {will_hit_wall_or_rock}")
                                break
                        case "<":
                            compare_bit = rock_indexes[current_rock_index][1] + 1
                            print(f"compare_bit: {compare_bit}")
                            if compare_bit < CHAMBER_WIDTH and not get_normalized_bit(
                                tunnel_map[i], compare_bit
                            ):
                                temp_tunnel_map[i] = tunnel_map[i] << 1
                                rock_indexes[current_rock_index] = (
                                    rock_indexes[current_rock_index][0] + 1,
                                    rock_indexes[current_rock_index][1] + 1,
                                )
                            else:
                                will_hit_wall_or_rock = True
                                print(f"will_hit_wall_or_rock: {will_hit_wall_or_rock}")
                                break
                        case _:
                            raise Exception("Invalid jet direction")

                if not will_hit_wall_or_rock:
                    for i, v in temp_tunnel_map.items():
                        tunnel_map[i] = v

                print(f"after: {rock_indexes}")
            print_tunnel_map(tunnel_map)
            # print("")

    # only shift rock bits
    return len(tunnel_map)


def part_2(data: InputData) -> int:
    return 0


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(pi)
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 0

    part2_answer = part_2(pi)
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
