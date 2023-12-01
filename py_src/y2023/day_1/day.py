from copy import deepcopy
import os
import re
from pathlib import Path
from typing import Generator, List


base_path = Path(__file__).parent

InputData = List[str]

replace_map = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

rex = r"(one|two|three|four|five|six|seven|eight|nine)"


def process_input(file: str) -> Generator[InputData, None, None]:
    with open(file, "r") as reader:
        for pairs in reader.read().split("\n\n"):
            return list(map(lambda val: val.strip(), pairs.splitlines()))


def get_calibration_digits(data: InputData) -> int:
    chars = [[s for s in line if s.isdigit()] for line in data]
    return list(map(lambda val: int(val[0] + val[-1]), chars))


def replace_words_with_numbers(data: InputData) -> InputData:
    while re.search(rex, data):
        result = re.search(rex, data)
        digit = replace_map[result.group(0)]
        data = re.sub(result.group(0), digit, data, 1)

    return data


def calculate_digits(line: InputData) -> int:
    result = []
    for i, char in enumerate(line):
        if char.isnumeric():
            result.append(char)
        else:
            for word, value in replace_map.items():
                if line[i:].startswith(word):
                    result.append(value)

    return result


def part_1(data: InputData) -> int:
    input = get_calibration_digits(data)
    return sum(input)


def part_2(data: InputData) -> int:
    sum = 0
    # parsed_input = [replace_words_with_numbers(line) for line in data]
    # result = get_calibration_digits(parsed_input)
    # print(result)
    # return sum(result)
    for line in data:
        digits = calculate_digits(line)
        sum += int(digits[0] + digits[-1])

    return sum


def main():
    pi = list(process_input(os.path.join(base_path, "input.txt")))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 55017

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer < 53551
    assert part2_answer == 53539


if __name__ == "__main__":
    main()
