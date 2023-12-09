from copy import deepcopy
import os
from pathlib import Path
from typing import List
import itertools
from functools import cmp_to_key
from enum import Enum

base_path = Path(__file__).parent


# TODO: refactoring to use a different scheme can simplify the problem to simple bit shifting
class HandRank(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 8
    FIVE_OF_A_KIND = 16


Hand = tuple[str, int]
InputData = List[Hand]
CharCounts = dict[int, list[str]]
HandMap = dict[int, list[Hand, CharCounts]]
RankedHands = dict[HandRank, list[Hand]]
CardValues = dict[str, int]


def apply_wilds(current_hand: Hand, joker_count: int) -> Hand:
    if joker_count < 1 or current_hand == HandRank.FIVE_OF_A_KIND:
        return current_hand

    wild_map = {
        1: {
            HandRank.FOUR_OF_A_KIND: HandRank.FIVE_OF_A_KIND,
            HandRank.THREE_OF_A_KIND: HandRank.FOUR_OF_A_KIND,
            HandRank.TWO_PAIR: HandRank.FULL_HOUSE,
            HandRank.ONE_PAIR: HandRank.THREE_OF_A_KIND,
            HandRank.HIGH_CARD: HandRank.ONE_PAIR,
        },
        2: {
            HandRank.THREE_OF_A_KIND: HandRank.FIVE_OF_A_KIND,
            HandRank.ONE_PAIR: HandRank.FOUR_OF_A_KIND,
            HandRank.HIGH_CARD: HandRank.THREE_OF_A_KIND,
        },
        3: {
            HandRank.ONE_PAIR: HandRank.FIVE_OF_A_KIND,
            HandRank.HIGH_CARD: HandRank.FOUR_OF_A_KIND,
        },
        4: {
            HandRank.HIGH_CARD: HandRank.FIVE_OF_A_KIND,
        },
        5: {
            HandRank.HIGH_CARD: HandRank.FIVE_OF_A_KIND,
        },
    }

    return wild_map[joker_count][current_hand]


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        for pairs in reader.read().split("\n\n"):
            return list(
                map(
                    lambda item: (item[0], int(item[1])),
                    map(lambda val: val.strip().split(" "), pairs.splitlines()),
                )
            )


def compare_hands_part_1(hand1: Hand, hand2: Hand) -> int:
    card_values: CardValues = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }
    for i in range(len(hand1[0])):
        h1_value = card_values[hand1[0][i]]
        h2_value = card_values[hand2[0][i]]
        if h1_value > h2_value:
            return 1
        elif h1_value < h2_value:
            return -1

    return 0


def compare_hands_part_2(hand1: Hand, hand2: Hand) -> int:
    card_values: CardValues = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
        "J": 1,
    }

    for i in range(len(hand1[0])):
        h1_value = card_values[hand1[0][i]]
        h2_value = card_values[hand2[0][i]]
        if h1_value > h2_value:
            return 1
        elif h1_value < h2_value:
            return -1

    return 0


def sort_hands(hands: RankedHands, compare_method) -> List[Hand]:
    sorted_hands = []
    for hand_list in hands.values():
        sorted_hand_list = sorted(hand_list, key=cmp_to_key(compare_method))
        sorted_hands += sorted_hand_list

    return sorted_hands


def calculate_total(ranked_hands: List[Hand]) -> int:
    total = 0
    for i, hand in enumerate(ranked_hands):
        _, bet = hand
        total += bet * (i + 1)

    return total


def get_ranked_hands() -> RankedHands:
    ranked_hands: RankedHands = {}

    for rank in HandRank:
        ranked_hands[rank.value] = []

    return ranked_hands


def part_1(data: InputData) -> int:
    ranked_hands = get_ranked_hands()

    for hand in data:
        cards, _ = hand
        total = HandRank.HIGH_CARD.value
        found_cards = {}
        for card in cards:
            if card not in found_cards:
                found_cards[card] = 1
            else:
                found_cards[card] += 1

        for card, count in found_cards.items():
            match count:
                case 5:
                    total += HandRank.FIVE_OF_A_KIND.value
                    break
                case 4:
                    total += HandRank.FOUR_OF_A_KIND.value
                    break
                case 3:
                    total += HandRank.THREE_OF_A_KIND.value
                case 2:
                    total += HandRank.ONE_PAIR.value
                # case _:
                #     print("high card")

        ranked_hands[total].append(hand)

    sorted_hands = sort_hands(ranked_hands, compare_hands_part_1)

    return calculate_total(sorted_hands)


def part_2(data: InputData) -> int:
    ranked_hands = get_ranked_hands()

    for hand in data:
        cards, _ = hand
        total = HandRank.HIGH_CARD.value
        found_cards = {}
        for card in cards:
            if card not in found_cards:
                found_cards[card] = 1
            else:
                found_cards[card] += 1

        wild_card_count = found_cards["J"] if "J" in found_cards else 0
        for card, count in found_cards.items():
            if card != "J":
                match count:
                    case 5:
                        total += HandRank.FIVE_OF_A_KIND.value
                        break
                    case 4:
                        total += HandRank.FOUR_OF_A_KIND.value
                        break
                    case 3:
                        total += HandRank.THREE_OF_A_KIND.value
                    case 2:
                        total += HandRank.ONE_PAIR.value

                # case _:
                #     print("high card")

        if wild_card_count > 0:
            total = apply_wilds(HandRank(total), wild_card_count).value

        ranked_hands[total].append(hand)

    sorted_hands = sort_hands(ranked_hands, compare_hands_part_2)

    return calculate_total(sorted_hands)


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 250474325

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 248909434


if __name__ == "__main__":
    main()
