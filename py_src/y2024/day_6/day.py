from copy import deepcopy
import os
from pathlib import Path
from typing import Generator, List


base_path = Path(__file__).parent

InputData = List[str]
Coord = tuple[int, int]
Position = tuple[Coord, Coord]


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        for pairs in reader.read().split("\n\n"):
            return list(map(lambda val: val.strip(), pairs.splitlines()))

def in_bounds(position: Coord, max_x: int, max_y: int) -> bool:
    x, y = position
    return 0 <= x < max_x and 0 <= y < max_y

def print_map(max_x: int, max_y: int, visited: set[Coord], obstacles: set[Coord], position: Position) -> None:
    for y in range(max_y):
        for x in range(max_x):
            if (x, y) in visited:
                print(".", end="")
            elif (x, y) in obstacles:
                print("#", end="")
            elif (x, y) == position[0]:
                print("X", end="")
            else:
                print(" ", end="")
        print()

def collect_data(data: InputData) -> tuple[set[Coord], Position]:
    obstacles: set[Coord] = set()   

    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == "^":
                position = ((x, y), (0, -1))
            elif char == "#":
                obstacles.add((x, y))   
    return (obstacles, position)


def patrol(visited: set[Position], obstacles: set[Coord], position: Position, max_x: int, max_y: int) -> tuple[set[Coord], bool]:
    is_loop = False
    patrolling = True

    while patrolling:
        coord, direction = position
        x, y = coord
        dir_x, dir_y = direction
        new_coord = (x + dir_x, y + dir_y)

        if not in_bounds(new_coord, max_x, max_y):
            patrolling = False
            break

        if new_coord in obstacles:
            direction = (-dir_y, dir_x)
            position = (coord, direction) 
        else:
            position = (new_coord, direction)
            if position in visited:
                is_loop = True
                patrolling = False
                break

            visited.add(position)

    return (visited, is_loop)


def part_1(data: InputData) -> int:
    obstacles, position = collect_data(data)
    visited: set[Position] = set()
    visited.add(position)

    (visited_list, _) = patrol(visited, obstacles, position, len(data[0]), len(data))
    visited.update(visited_list)

    unique_visited = set(map(lambda x: x[0], visited))

    # print_map(len(data[0]), len(data), visited, obstacles, position)
    return len(unique_visited)


def part_2(data: InputData) -> int:
    orig_obstacles, position = collect_data(data)
    tried_positions = set() 
    potential_positions = set()
    
    visited = set([position])
    path_coords, is_loop = patrol(visited, orig_obstacles, position, len(data[0]), len(data))
    
    for pos, _ in path_coords:
        if pos != position[0]:  
            potential_positions.add(pos)
    
    loop_count = 0
    for test_pos in potential_positions:
        if test_pos in tried_positions:
            continue
            
        obstacles = deepcopy(orig_obstacles)
        obstacles.add(test_pos)
        visited = set([position])
        
        path_coords, is_loop = patrol(visited, obstacles, position, len(data[0]), len(data))
        tried_positions.add(test_pos)
        
        if is_loop:
            loop_count += 1
    
    return loop_count


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer > 4818
    assert part1_answer == 4819

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 1796


if __name__ == "__main__":
    main()
