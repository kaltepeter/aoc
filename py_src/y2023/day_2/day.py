from copy import deepcopy
import os
import re
from pathlib import Path
from typing import Generator, Tuple, Dict


base_path = Path(__file__).parent

Round = Tuple[int, int, int]
InputData = Dict[int, Round]


def extract_tuple(line: str) -> Round:
    red = re.search(r"(\d+) red", line)
    green = re.search(r"(\d+) green", line)
    blue = re.search(r"(\d+) blue", line)

    return tuple(
        [
            int(red.group(1)) if red else 0,
            int(green.group(1)) if green else 0,
            int(blue.group(1)) if blue else 0,
        ]
    )


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        for pairs in reader.read().split("\n\n"):
            lines = list(map(lambda val: val.strip(), pairs.splitlines()))
            games = [line.split(":") for line in lines]
            return {
                int(game[0].replace("Game ", "").strip()): list(
                    map(
                        lambda val: extract_tuple(val.strip()),
                        game[1].strip().split(";"),
                    )
                )
                for game in games
            }


def filter_games(
    data: InputData, max_red: int, max_green: int, max_blue: int
) -> InputData:
    valid_games = set()
    for game, rounds in data.items():
        valid = True
        for round in rounds:
            # Filter games where any round exceeds limits
            if round[0] > max_red or round[1] > max_green or round[2] > max_blue:
                valid = False
                break

        if valid:
            valid_games.add(game)

    return valid_games


def part_1(data: InputData) -> int:
    valid_games = filter_games(data, 12, 13, 14)
    return sum(valid_games)


def part_2(data: InputData) -> int:
    game_power = []
    for rounds in data.values():
        min_red = max(round[0] for round in rounds)
        min_green = max(round[1] for round in rounds)
        min_blue = max(round[2] for round in rounds)
        game_power.append(min_red * min_green * min_blue)

    return sum(game_power)


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 2204

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
