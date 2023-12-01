import os
from pathlib import Path
from .day import (
    Move,
    RoundResult,
    calc_game_score,
    calc_score,
    part_1,
    part_2,
    process_input,
    who_won,
)

base_path = Path(__file__).parent


def test_calc_game_score():
    assert calc_game_score([(1, 8), (8, 1), (6, 6)]) == (15, 15)
    assert calc_game_score([(1, 8), (2, 3), (6, 6)]) == (9, 17)


def test_get_move_from_key():
    assert Move.get_move_from_key("A") == Move.ROCK
    assert Move.get_move_from_key("X") == Move.ROCK
    assert Move.get_move_from_key("B") == Move.PAPER
    assert Move.get_move_from_key("Y") == Move.PAPER
    assert Move.get_move_from_key("C") == Move.SCISSORS
    assert Move.get_move_from_key("Z") == Move.SCISSORS


def test_get_round_result_from_key():
    assert RoundResult.get_round_result_from_key("Y") == RoundResult.DRAW
    assert RoundResult.get_round_result_from_key("X") == RoundResult.LOST
    assert RoundResult.get_round_result_from_key("Z") == RoundResult.WON


def test_get_move_from_result():
    assert Move.get_move_from_result(Move.ROCK, RoundResult.DRAW) == Move.ROCK
    assert Move.get_move_from_result(Move.PAPER, RoundResult.LOST) == Move.ROCK
    assert Move.get_move_from_result(Move.SCISSORS, RoundResult.WON) == Move.ROCK


def test_calc_score():
    assert calc_score(Move.PAPER, RoundResult.WON) == 8
    assert calc_score(Move.ROCK, RoundResult.LOST) == 1
    assert calc_score(Move.SCISSORS, RoundResult.DRAW) == 6


def test_who_won():
    assert who_won(Move.ROCK, Move.PAPER, 2) == RoundResult.WON
    assert who_won(Move.ROCK, Move.PAPER, 1) == RoundResult.LOST
    assert who_won(Move.ROCK, Move.ROCK, 2) == RoundResult.DRAW
    assert who_won(Move.ROCK, Move.SCISSORS, 2) == RoundResult.LOST
    assert who_won(Move.SCISSORS, Move.ROCK, 1) == RoundResult.LOST


def test_process_input():
    assert process_input(os.path.join(base_path, "example.txt")) == [
        (Move.ROCK.value[0], Move.PAPER.value[1]),
        (Move.PAPER.value[0], Move.ROCK.value[1]),
        (Move.SCISSORS.value[0], Move.SCISSORS.value[1]),
    ]


def test_part_1():
    game = process_input(os.path.join(base_path, "example.txt"))
    assert part_1(game) == 15


def test_part_2():
    game = process_input(os.path.join(base_path, "example.txt"))
    assert part_2(game) == 12
