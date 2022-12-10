import os
from pathlib import Path
from typing import List, Literal, Tuple


base_path = Path(__file__).parent

Position = Tuple[int, int]
Dir = Literal["U", "D", "L", "R"]
Move = Tuple[Dir, int]
Moves = List[Move]


def move(pos: Position, move: Move) -> Position:
    dir, distance = move
    if dir == "U":
        return (pos[0], pos[1] - distance)
    elif dir == "D":
        return (pos[0], pos[1] + distance)
    elif dir == "L":
        return (pos[0] - distance, pos[1])
    elif dir == "R":
        return (pos[0] + distance, pos[1])
    else:
        raise Exception(f"Unknown direction: {dir}")


def is_touching(h: Position, t: Position, max_distance: int = 1) -> bool:
    touching = False
    neighbors = [
        (x, y) for x in range(h[0] - 1, h[0] + 2) for y in range(h[1] - 1, h[1] + 2)
    ]
    if t in neighbors:
        touching = True
    return touching


def get_diag(h: Position, t: Position) -> Position:
    diags = [
        (t[0] - 1, t[1] - 1),
        (t[0] + 1, t[1] - 1),
        (t[0] - 1, t[1] + 1),
        (t[0] + 1, t[1] + 1),
    ]
    pos = [d for d in diags if is_touching(h, d)]
    if len(pos) > 1:
        raise Exception(f"More than one diag: {pos}")
    else:
        return pos


def process_input(file: str) -> Moves:
    with open(file) as reader:
        lines = reader.read().strip().split("\n")
        return [(line[0], int(line[1:])) for line in lines]


def part_1(moves: Moves) -> int:
    visited = set()
    s = (0, 0)
    h = s
    t = s
    for idx, m in enumerate(moves):
        prev_m = moves[idx - 1] if idx > 0 else ()
        # print(f"move: {m} prev_move: {prev_m} h:{h} t:{t}")
        for i in range(m[1]):
            h = move(h, (m[0], 1))

            if h[0] != t[0] and h[1] != t[1] and not is_touching(h, t):
                t = get_diag(h, t)[0]

            if not is_touching(h, t):
                t = move(t, (m[0], 1))

            #  catch error
            if not is_touching(h, t):
                raise ValueError("Too far away")

            visited.add(t)

        # print(f"head: {h} tail: {t}")
        # print()

    return len(visited)


def part_2(moves: Moves) -> int:
    return 0


def main():
    file_tree = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(file_tree)
    print(f"Part I: {part1_answer} spaces visited")
    assert part1_answer == 6023

    part2_answer = part_2(file_tree)
    print(f"Part II: {part2_answer} spaces visited")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
