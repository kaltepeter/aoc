from copy import deepcopy
from functools import cache, reduce
from operator import mul
import os
from pathlib import Path
from typing import Generator, List
import re

base_path = Path(__file__).parent

Coord = tuple[int, int]
Velocity = tuple[int, int]
Robot = tuple[Coord, Velocity]
InputData = List[Robot]


def process_input(file: str) -> InputData:
    robots = []
    with open(file, "r") as reader:
        for line in reader.read().splitlines():
            pos_match = re.search(r"p=(\d+),(\d+)", line)
            vel_match = re.search(r"v=(-?\d+),(-?\d+)", line)
            pos = (int(pos_match.group(1)), int(pos_match.group(2)))
            vel = (int(vel_match.group(1)), int(vel_match.group(2)))
            robots.append((pos, vel))
            
    return robots


# @cache
def move_robots(robots: InputData, max_x: int, max_y: int, iterations: int = 1) -> InputData:
    new_robots = []
    for (pos, vel) in robots:
        next_x = (pos[0] + (iterations * vel[0])) % max_x
        next_y = (pos[1] + (iterations * vel[1])) % max_y

        next_pos = (next_x, next_y) 
        new_robots.append((next_pos, vel))

    return new_robots


def get_quadrant(pos: Coord, max_x: int, max_y: int) -> int:
    (x, y) = pos
    quad_x = max_x // 2
    quad_y = max_y // 2

    if 0 <= x < quad_x:
        if 0 <= y < quad_y:
            return 1
        elif (max_y - quad_y) <= y <= max_y:
            return 3
        
    elif (max_x - quad_x) <= x <= max_x:
        if 0 <= y < quad_y:
            return 2
        elif (max_y - quad_y) <= y <= max_y:
            return 4
        
    return 0


def print_robot_positions(positions: List[Coord], width: int, height: int) -> Generator[str, None, None]:
    grid = [['.'] * width for _ in range(height)]
    
    for x, y in positions:
        grid[y][x] = '#'
    
    for row in grid:
        yield(''.join(row))


def part_1(data: InputData) -> int:
    width = 101
    height = 103

    cur_paths = move_robots(data, width, height, 100)

    quadrants = {1: [], 2: [], 3: [], 4: []}
    for pos, _ in cur_paths:
        quad = get_quadrant(pos, width, height)
        if quad > 0:
            quadrants[quad].append(pos)


    return reduce(mul, map(len, quadrants.values()))


def part_2(data: InputData) -> int:
    width = 101
    height = 103

# ugh... in theory the lowest calcuation would be it, didn't work
    with open(os.path.join(base_path, 'output.txt'), "w") as writer:
        cur_paths = deepcopy(data)
        for i in range(1, width * height):
            cur_paths = move_robots(cur_paths, width, height)
            paths = [pos for pos, _ in cur_paths]
            writer.write(f"iteration {i}\n")
            for line in print_robot_positions(paths, width, height):
                writer.write(f"{line}\n")


    known_iteration = 7569
    print_iteration = move_robots(data, width, height, known_iteration)
    paths = [pos for pos, _ in print_iteration]
    for line in print_robot_positions(paths, width, height):
        print(f"{line}\n")
    
    return known_iteration


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer < 697767840
    assert part1_answer == 232589280

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer > 7568
    assert part2_answer == 7569


if __name__ == "__main__":
    main()
