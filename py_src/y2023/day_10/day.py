from copy import deepcopy
import os
from pathlib import Path
from typing import Generator, List
from enum import Enum
import numpy as np
from collections import deque

base_path = Path(__file__).parent


class CharMap(Enum):
    EMPTY = "."
    START = "S"
    PIPE = "|"
    DASH = "-"
    EL = "L"
    JAY = "J"
    SEVEN = "7"
    EFF = "F"


PipeMap = List[str]
InputData = List[PipeMap]
# x, y
Coord = tuple[int, int]
StartPipe = tuple[Coord, CharMap]


pipe_map = {
    (0, 1): [CharMap.PIPE, CharMap.SEVEN, CharMap.EFF],
    (0, -1): [CharMap.PIPE, CharMap.EL, CharMap.JAY],
    (1, 0): [CharMap.DASH, CharMap.EL, CharMap.EFF],
    (-1, 0): [CharMap.DASH, CharMap.JAY, CharMap.SEVEN],
}

path_map = {
    CharMap.PIPE: [(0, -1), (0, 1)],
    CharMap.DASH: [(-1, 0), (1, 0)],
    CharMap.EL: [(0, -1), (1, 0)],
    CharMap.JAY: [(0, -1), (-1, 0)],
    CharMap.SEVEN: [(0, 1), (-1, 0)],
    CharMap.EFF: [(0, 1), (1, 0)],
}


def lookup_char(coord: Coord, neighbor_1: Coord, neighbor_2: Coord) -> CharMap:
    x1 = 1 if neighbor_1[0] > coord[0] else 0 if neighbor_1[0] == coord[0] else -1
    y1 = 1 if neighbor_1[1] > coord[1] else 0 if neighbor_1[1] == coord[1] else -1
    x2 = 1 if neighbor_2[0] > coord[0] else 0 if neighbor_2[0] == coord[0] else -1
    y2 = 1 if neighbor_2[1] > coord[1] else 0 if neighbor_2[1] == coord[1] else -1

    coord1 = (x1, y1)
    coord2 = (x2, y2)

    return list(set(pipe_map[coord1]) & set(pipe_map[coord2]))[0]


def process_input(file: str) -> Generator[InputData, None, None]:
    with open(file, "r") as reader:
        for pairs in reader.read().split("\n\n"):
            yield list(map(lambda val: val.strip(), pairs.splitlines()))


def get_neighbor_coords(
    coord: Coord, x_range: tuple[int, int], y_range: tuple[int, int]
) -> List[Coord]:
    coords = []
    if coord[0] - 1 >= x_range[0]:
        coords.append((coord[0] - 1, coord[1]))

    if coord[0] + 1 <= x_range[1]:
        coords.append((coord[0] + 1, coord[1]))

    if coord[1] - 1 >= y_range[0]:
        coords.append((coord[0], coord[1] - 1))

    if coord[1] + 1 <= y_range[1]:
        coords.append((coord[0], coord[1] + 1))

    # for y in range(max(coord[1] - 1, y_range[0]), min(coord[1] + 1, y_range[1])):
    #     for x in range(max(coord[0] - 1, x_range[0]), min(coord[0] + 1, x_range[1])):
    #         if (x, y) != coord:
    #             coords.append((x, y))

    return coords


def calculate_start_pipe(data: InputData) -> StartPipe:
    start_pipe = [(0, 0), ""]
    for y, row in enumerate(data):
        for x, col in enumerate(row):
            if col == "S":
                start_pipe[0] = (x, y)
                break
        else:
            continue
        break

    neighbors = get_neighbor_coords(start_pipe[0], (0, len(data[0])), (0, len(data)))
    connected_pipes = []
    for x, y in neighbors:
        direction = np.subtract(start_pipe[0], (x, y))
        # print(
        #     direction,
        #     data[y][x],
        #     CharMap(data[y][x]) in pipe_map[(direction[0], direction[1])],
        # )
        if (
            data[y][x] != CharMap.EMPTY.value
            and CharMap(data[y][x]) in pipe_map[(direction[0], direction[1])]
        ):
            connected_pipes.append((x, y))

        if len(connected_pipes) == 2:
            break

    # print(start_pipe[0], connected_pipes)
    start_pipe[1] = lookup_char(start_pipe[0], connected_pipes[0], connected_pipes[1])

    return start_pipe


# def get_connected_pipes(pipe_map: InputData, coord: Coord)


def get_coord(prev_coord: Coord, path: Coord) -> Coord:
    return (prev_coord[0] + path[0], prev_coord[1] + path[1])


def find_loop(
    data: InputData, visited_pipes: set[Coord], start_pipe: StartPipe
) -> set[Coord]:
    q = deque([start_pipe[0]])

    char = start_pipe[1]
    start_path = path_map[char][-1]
    directions = [start_path]
    prev_char = char
    prev_coord = start_pipe[0]

    while q:
        x, y = q.popleft()
        char = CharMap(data[y][x])

        if char == CharMap.START:
            char = start_pipe[1]

        directions = path_map[char]

        for direction in directions:
            next_pipe = get_coord((x, y), direction)
            if (
                next_pipe == start_pipe[0]
                and prev_char != start_pipe[1]
                and prev_coord != start_pipe[0]
            ):
                break

            if next_pipe in visited_pipes:
                continue

            if next_pipe not in visited_pipes:
                visited_pipes.add(next_pipe)
                q.append(next_pipe)

        prev_char = char
        prev_coord = (x, y)

    return visited_pipes


# http://philliplemons.com/posts/ray-casting-algorithm
# https://www.youtube.com/watch?v=zhmzPQwgPg0
# has edge cases
def count_inversions(visited: set[Coord], line: str, x: int, y: int) -> int:
    count = 0
    for idx in range(x):
        if not (idx, y) in visited:
            continue

        count += line[idx] in {CharMap.PIPE.value, CharMap.EL.value, CharMap.JAY.value}

    return count


def part_1(data: InputData) -> int:
    start_pipe = calculate_start_pipe(data)
    print(start_pipe)
    visited_pipes = find_loop(data, {start_pipe[0]}, start_pipe)

    return len(visited_pipes) / 2


def part_2(data: InputData) -> int:
    start_pipe = calculate_start_pipe(data)
    print(start_pipe)
    visited_pipes = find_loop(data, {start_pipe[0]}, start_pipe)
    # print(visited_pipes)

    start_row = data[start_pipe[0][1]]
    data[start_pipe[0][1]] = start_row.replace(
        CharMap.START.value, start_pipe[1].value, start_pipe[0][0]
    )

    count = 0
    for y, row in enumerate(data):
        for x, _ in enumerate(row):
            if not (x, y) in visited_pipes:
                inversions = count_inversions(visited_pipes, row, x, y)
                # print(f"inversions: {inversions}, {inversions % 2}")
                if inversions % 2 == 1:
                    count += 1

    return count


def main():
    pi = list(process_input(os.path.join(base_path, "input.txt")))[0]

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 6903

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer < 2836
    assert part2_answer < 273
    assert part2_answer == 265


if __name__ == "__main__":
    main()
