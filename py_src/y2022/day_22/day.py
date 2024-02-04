from copy import deepcopy
import os
from pathlib import Path
from typing import List, Union, Generator
from enum import Enum
import re

base_path = Path(__file__).parent


class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


Board = List[str]
Path = List[Union[int, str]]
InputData = tuple[Board, Path]
Position = tuple[int, int, Direction]
WALL = "#"
EMPTY = " "
RangeList = dict[int, tuple[int, int]]

dir_chars = {
    Direction.RIGHT: ">",
    Direction.DOWN: "v",
    Direction.LEFT: "<",
    Direction.UP: "^",
}

dir_map = {
    Direction.RIGHT: (1, 0),
    Direction.DOWN: (0, 1),
    Direction.LEFT: (-1, 0),
    Direction.UP: (0, -1),
}


def replace_char_at_index(org_str: str, index: int, replacement: str):
    """Replace character at index in string org_str with the
    given replacement character."""
    new_str = org_str
    if index < len(org_str):
        # print(index, index + 1, len(org_str))
        new_str = org_str[0:index] + replacement + org_str[index + 1 :]
    return new_str


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        board, key = reader.read().split("\n\n")
        parts = [part for part in re.split(r"(\d+)", key.strip()) if part]
        path: Path = [int(item) if item.isdigit() else item for item in parts]
        return (board.splitlines(), path)


def calculate_pw(row: int, col: int, facing: Direction) -> int:
    return sum([(1000 * row), (4 * col), facing.value])


def print_path(board: Board, path) -> None:
    for y, row in enumerate(board):
        # print("y", y, len(row))
        for x, direction in path.get(y, []):
            row = replace_char_at_index(row, x, dir_chars[direction])

        print(row)


def get_ranges(board: Board) -> RangeList:
    ranges: RangeList = {}
    for y, row in enumerate(board):
        hash_positions = [i for i, c in enumerate(row) if c == "#"]
        dot_positions = [i for i, c in enumerate(row) if c == "."]

        all_positions = hash_positions + dot_positions
        min_pos = min(all_positions) if all_positions else 0
        max_pos = max(all_positions) if all_positions else 0

        ranges[y] = (min_pos, max_pos)

    return ranges


def part_1(data: InputData) -> int:
    board, path = data

    width = max(map(len, board))
    board = [line + " " * (width - len(line)) for line in board]

    x = board[0].index(".")
    y = 0
    facing = Direction.RIGHT
    route: dict[int, List[tuple[int, Direction]]] = {0: [(x, Direction.RIGHT)]}

    for p in path:
        if isinstance(p, (int, float, complex)):
            for _ in range(p):
                dc, dr = dir_map[facing]
                next_x = x
                next_y = y
                while True:
                    next_y = (next_y + dr) % len(board)
                    next_x = (next_x + dc) % len(board[0])
                    if board[next_y][next_x] != EMPTY:
                        break
                if board[next_y][next_x] == WALL:
                    break

                x = next_x
                y = next_y

                if y not in route:
                    route[y] = []

                route[y].append((x, facing))
        else:
            if y not in route:
                route[y] = []
            new_dir = 1 if p == "R" else -1
            new_val = (facing.value + new_dir) % len(Direction)
            facing = Direction(new_val)
            route[y].append((x, facing))

    # print_path(board, route)

    return calculate_pw(y + 1, x + 1, facing)


# def part_1(data: InputData) -> int:
#     board, path = data
#     open_tiles = set()
#     walls = set()
#     empty_space = set()

#     for y, row in enumerate(board):
#         for x, col in enumerate(row):
#             if col == ".":
#                 open_tiles.add((x, y))
#             elif col == WALL:
#                 walls.add((x, y))
#             else:
#                 empty_space.add((x, y))

#     x = board[0].index(".")
#     y = 0
#     facing = Direction.RIGHT
#     route: dict[int, List[tuple[int, Direction]]] = {0: [(x, Direction.RIGHT)]}
#     ranges = get_ranges(board)
#     max_y = len(board) - 1

#     for p in path:
#         print(f"p: {p}")
#         if isinstance(p, (int, float, complex)):
#             print_path(board, route)
#             print("")
#             for _ in range(p):
#                 r = ranges[y]
#                 if board[y][x] == ".":
#                     last_y = y
#                     last_x = x
#                 print(f"i: {x, y, facing}")
#                 match facing:
#                     case Direction.RIGHT:
#                         x += 1
#                         if (x, y) in walls:
#                             x -= 1
#                         elif x > r[1]:
#                             x = r[0]
#                     case Direction.DOWN:
#                         y += 1
#                         if (x, y) in walls:
#                             y -= 1
#                         elif y > max_y:
#                             y = 0

#                         if (x, y) in empty_space:
#                             y = last_y
#                             continue

#                 if y not in route:
#                     route[y] = []

#                 route[y].append((x, facing))
#         else:
#             if y not in route:
#                 route[y] = []

#             new_dir = 1 if p == "R" else -1
#             new_val = (facing.value + new_dir) % len(Direction)
#             facing = Direction(new_val)
#             route[y].append((x, facing))

#     return calculate_pw(y + 1, x + 1, facing)


# def part_1(data: InputData) -> int:
#     board, path = data
#     # min/maxes per row
#     ranges = get_ranges(board)
#     max_y = len(board) - 1

#     x = board[0].index(".")
#     y = 0
#     facing = Direction.RIGHT
#     route: dict[int, List[tuple[int, Direction]]] = {0: [(x, Direction.RIGHT)]}


#     for p in path:
#         # print(f"p: {p}")
#         if isinstance(p, (int, float, complex)):
#             # print_path(board, route)
#             # print("")
#             # TODO: short circuit look ahead. use index of next wall
#             for _ in range(p):
#                 r = ranges[y]
#                 # print(f"r {r}")
#                 # print(f"i: {y, x, facing}")
#                 match facing:
#                     case Direction.RIGHT:
#                         next_x = x + 1
#                         if next_x > r[1]:
#                             next_x = r[0]
#                         cell = board[y][next_x]
#                         if cell == WALL:
#                             break
#                         else:
#                             x = next_x
#                     case Direction.DOWN:
#                         next_y = y + 1
#                         if next_y > max_y:
#                             next_y = abs(max_y - next_y)
#                         elif board[next_y][x] == WALL:
#                             break

#                         cell = board[next_y][x]
#                         if cell == WALL:
#                             break
#                         else:
#                             y = next_y
#                     case Direction.LEFT:
#                         next_x = x - 1
#                         if next_x < r[0]:
#                             next_x = r[1]
#                         cell = board[y][next_x]
#                         if cell == WALL:
#                             break
#                         else:
#                             x = next_x
#                     case Direction.UP:
#                         next_y = y - 1
#                         if next_y < 0:
#                             y = max_y
#                         cell = board[next_y][x]
#                         if cell == WALL:
#                             break
#                         else:
#                             y = next_y
#                 if y not in route:
#                     route[y] = []

#                 # TODO: ........#... range depends on left or right of hash

#                 # print(f"y: {y} x: {x} facing: {facing}")
#                 if board[y][x] != EMPTY:
#                     route[y].append((x, facing))
#             # print("yo")
#         else:
#             new_dir = 1 if p == "R" else -1
#             new_val = (facing.value + new_dir) % len(Direction)
#             facing = Direction(new_val)
#             route[y].append((x, facing))

#     return calculate_pw(y + 1, x + 1, facing)


def part_2(data: InputData) -> int:
    return 0


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 1484

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
