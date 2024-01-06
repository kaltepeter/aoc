from copy import deepcopy
import os
from pathlib import Path
from typing import List, Deque
from collections import deque


base_path = Path(__file__).parent

Location = tuple[int, int]
# start pos, grid
InputData = tuple[Location, List[str]]
START = "S"
ROCK = "#"


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        grid = reader.read().splitlines()
        start = next(
            (x, y)
            for y, row in enumerate(grid)
            for x, char in enumerate(row)
            if char == START
        )
        return (start, grid)


def in_bounds(location: Location, max_x: int, max_y: int) -> bool:
    x, y = location
    return 0 <= x < max_x and 0 <= y < max_y


def get_neighbors(location: Location, max_x: int, max_y: int) -> List[Location]:
    x, y = location
    neighbors = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]
    return filter(lambda location: in_bounds(location, max_x, max_y), neighbors)


def part_1(data: InputData, goal: int) -> int:
    start, grid = data
    seen = {start}
    result = set()
    # (x, y, steps)
    q: Deque[tuple[int, int, int]] = deque([(*start, goal)])

    while q:
        x, y, step = q.popleft()

        if step % 2 == 0:
            result.add((x, y))

        if step == 0:
            continue

        for nx, ny in get_neighbors((x, y), len(grid[0]), len(grid)):
            n_loc = (nx, ny)
            if n_loc in seen or grid[ny][nx] == ROCK:
                continue

            seen.add(n_loc)
            q.append((nx, ny, step - 1))

    return len(result)


def part_2(data: InputData) -> int:
    return 0


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi), 64)
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 3795

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
