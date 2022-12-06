import os
from pathlib import Path
from typing import List


base_path = Path(__file__).parent


def check_unique(s: str) -> bool:
    return len(s) == len(set(s))


def process_input(file: str) -> List[str]:
    with open(file) as reader:
        return reader.read().strip().split("\n")


def part_1(data: str) -> int:
    packet_length = 4
    for i in range(len(data)):
        # print(f"for i={i}, data[i:i+3]={data[i:i+packet_length]}")
        if check_unique(data[i : i + packet_length]):
            return i + packet_length
    return 0


def part_2(data: str) -> int:
    packet_length = 14
    for i in range(len(data)):
        # print(f"for i={i}, data[i:i+3]={data[i:i+packet_length]}")
        if check_unique(data[i : i + packet_length]):
            return i + packet_length
    return 0


def main():
    signal_data = process_input(os.path.join(base_path, "input.txt"))[0]

    part1_answer = part_1(signal_data)
    print(f"Part I: {part1_answer} characters")
    assert part1_answer == 1275

    part2_answer = part_2(signal_data)
    print(f"Part II: {part2_answer} characters")
    assert part2_answer == 3605


if __name__ == "__main__":
    main()
