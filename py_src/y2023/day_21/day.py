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


def get_neighbors_infinite(location: Location) -> List[Location]:
    x, y = location
    neighbors = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]
    return neighbors


def fill(data: InputData, goal: int) -> int:
    start, grid = data
    seen: set[Location] = {start}
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


def part_1(data: InputData, goal: int) -> int:
    result = fill(data, goal)
    return result


def part_2(data: InputData, goal: int) -> int:
    start, grid = data
    x, y = start
    result = 0
    # assumptions
    assert len(grid) == len(grid[0])  # grid is square
    size = len(grid)
    assert x == y == size // 2  # start is center
    if size > 11:
        assert goal % size == size // 2  # steps reaches end of a grid
    print(goal // size)  # hint on solution
    grid_width = goal // size - 1

    odd = (grid_width // 2 * 2 + 1) ** 2
    even = ((grid_width + 1) // 2 * 2) ** 2
    odd_points = fill(((x, y), grid), size * 2 + 1)
    even_points = fill(((x, y), grid), size * 2)

    corner_t = fill(((x, size - 1), grid), size - 1)
    corner_r = fill(((0, y), grid), size - 1)
    corner_b = fill(((x, 0), grid), size - 1)
    corner_l = fill(((size - 1, y), grid), size - 1)

    small_size = size // 2 - 1
    small_tr = fill(((0, size - 1), grid), small_size)
    small_tl = fill(((size - 1, size - 1), grid), small_size)
    small_br = fill(((0, 0), grid), small_size)
    small_bl = fill(((size - 1, 0), grid), small_size)

    large_size = size * 3 // 2 - 1
    large_tr = fill(((0, size - 1), grid), large_size)
    large_tl = fill(((size - 1, size - 1), grid), large_size)
    large_br = fill(((0, 0), grid), large_size)
    large_bl = fill(((size - 1, 0), grid), large_size)

    # result, seen = fill(data, goal)
    result += odd * odd_points
    result += even * even_points
    result += corner_t + corner_r + corner_b + corner_l
    result += (grid_width + 1) * (small_tr + small_tl + small_br + small_bl)
    result += grid_width * (large_tr + large_tl + large_br + large_bl)

    return result


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi), 64)
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 3795

    part2_answer = part_2(deepcopy(pi), 26501365)
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 630129824772393


if __name__ == "__main__":
    main()
