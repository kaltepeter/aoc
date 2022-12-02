from enum import Enum
import os
from pathlib import Path
from typing import List, Tuple


base_path = Path(__file__).parent

Round = Tuple[str, str]
Game = List[Round]
Scores = List[Tuple[int, int]]


class RoundResult(Enum):
    LOST = 0
    DRAW = 3
    WON = 6

    @staticmethod
    def get_round_result_from_key(key: str) -> "RoundResult":
        if key == "Y":
            return RoundResult.DRAW
        elif key == "X":
            return RoundResult.LOST
        elif key == "Z":
            return RoundResult.WON
        else:
            raise ValueError(f"Invalid key: {key}")


class Move(Enum):
    ROCK = ("A", "X", 1)
    PAPER = ("B", "Y", 2)
    SCISSORS = ("C", "Z", 3)

    @staticmethod
    def get_move_from_key(key: str) -> "Move":
        for move in Move:
            if move.value[0] == key or move.value[1] == key:
                return move
        raise ValueError(f"Invalid key: {key}")

    @staticmethod
    def get_move_from_result(p1_move: "Move", result: RoundResult) -> "Move":
        # lookup move, move: (won, lost)
        move_list = {
            Move.ROCK: (Move.PAPER, Move.SCISSORS),
            Move.PAPER: (Move.SCISSORS, Move.ROCK),
            Move.SCISSORS: (Move.ROCK, Move.PAPER),
        }

        if result == RoundResult.DRAW:
            return p1_move
        elif result == RoundResult.LOST:
            return move_list[p1_move][1]
        elif result == RoundResult.WON:
            return move_list[p1_move][0]

        raise ValueError(f"Invalid result: {result}")


def calc_game_score(scores: Scores) -> Tuple[int, int]:
    return (sum(s[0] for s in scores), sum(s[1] for s in scores))


def calc_score(move: Move, res: RoundResult) -> int:
    return move.value[2] + res.value


def who_won(p1_move: Move, p2_move: Move, player: int) -> RoundResult:
    p = p2_move if player == 2 else p1_move
    other_p = p2_move if player == 1 else p1_move

    if other_p == p:
        return RoundResult.DRAW
    else:
        if p == Move.SCISSORS:
            return other_p == Move.PAPER and RoundResult.WON or RoundResult.LOST
        elif p == Move.ROCK:
            return other_p == Move.SCISSORS and RoundResult.WON or RoundResult.LOST
        elif p == Move.PAPER:
            return other_p == Move.ROCK and RoundResult.WON or RoundResult.LOST


def process_input(file: str) -> Game:
    with open(file) as reader:
        game_data = reader.read().strip().split("\n")
        return [tuple(round.split(" ")) for round in game_data]


def part_1(game: Game) -> int:
    scores: List[int] = []
    for round in game:
        p2_move = Move.get_move_from_key(round[1])
        my_result = who_won(Move.get_move_from_key(round[0]), p2_move, 2)
        scores += [(0, calc_score(p2_move, my_result))]

    return calc_game_score(scores)[1]


def part_2(game: Game) -> int:
    scores: List[int] = []
    for round in game:
        res = RoundResult.get_round_result_from_key(round[1])
        p1_move = Move.get_move_from_key(round[0])
        p2_move = Move.get_move_from_result(p1_move, res)
        my_result = who_won(p1_move, p2_move, 2)
        scores += [(0, calc_score(p2_move, my_result))]

    return calc_game_score(scores)[1]


def main():
    game = process_input(os.path.join(base_path, "input.txt"))

    print(f"Part I: {part_1(game)} is your score")

    print(f"Part II: {part_2(game)} is your score")


if __name__ == "__main__":
    main()
