from copy import deepcopy
import os
import re
from pathlib import Path
from typing import Generator, List


base_path = Path(__file__).parent

InputData = List[tuple[set[int], set[int]]]


def process_input(file: str) -> Generator[InputData, None, None]:
    with open(file, "r") as reader:
        for cards in reader.read().split("\n"):
            values = re.sub(r"Card\s+\d+: ", "", cards).split(" | ")
            if len(values) < 2:
                continue

            winning_nums = set(map(int, values[0].strip().split()))
            nums = set(map(int, values[1].strip().split()))
            yield (winning_nums, nums)


def calculate_card_points(winning_nums: set[int]) -> int:
    score = 0
    for i, _ in enumerate(winning_nums):
        if i == 0:
            score += 1
        else:
            score = 2 * score

    return score


def calculate_score(winners: List[set[int]]):
    scores = []
    for nums in list(winners):
        scores.append(calculate_card_points(nums))

    return sum(scores)


def part_1(data: InputData) -> int:
    winning_cards = []
    for card in list(data):
        winners = card[0] & card[1]
        if winners:
            winning_cards.append(card[0] & card[1])

    return calculate_score(winning_cards)


def part_2(data: InputData) -> int:
    all_cards = {}
    for i, card in enumerate(data):
        winners = card[0] & card[1]
        all_cards[i] = [winners, 1]

    for i, card in all_cards.items():
        for _ in range(card[1]):
            # loop through next cards equal to count of winning numbers
            for num in range(1, len(card[0]) + 1):
                all_cards[i + num][1] += 1

    return sum([v[1] for v in all_cards.values()])


def main():
    pi = list(process_input(os.path.join(base_path, "input.txt")))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 17782

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 8477787


if __name__ == "__main__":
    main()
