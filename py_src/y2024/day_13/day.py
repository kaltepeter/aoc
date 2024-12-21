from copy import deepcopy
import os
from pathlib import Path
from typing import List
import re

base_path = Path(__file__).parent

Coord = tuple[int, int]
# (prize_coord, a_coord, b_coord)
InputData = List[tuple[Coord, Coord, Coord]]


def process_input(file: str) -> InputData:
    machines = []
    with open(file, "r") as reader:
        for machine in reader.read().split("\n\n"):
            a, b, prize = machine.splitlines()
            a_match = re.search(r"Button A: X\+(\d+), Y\+(\d+)", a)
            b_match = re.search(r"Button B: X\+(\d+), Y\+(\d+)", b)
            p_match = re.search(r"Prize: X=(\d+), Y=(\d+)", prize)

            a_coord = (int(a_match.group(1)), int(a_match.group(2)))
            b_coord = (int(b_match.group(1)), int(b_match.group(2)))
            prize_coord = (int(p_match.group(1)), int(p_match.group(2)))

            machines.append((prize_coord, a_coord, b_coord))

    return machines 


def find_steps_to_goal(a_interval: Coord, b_interval: Coord, goal: Coord) -> tuple[int, int]:
    ax, ay = a_interval
    bx, by = b_interval
    goal_x, goal_y = goal

    # Using matrix algebra to solve:
    # m * ax + n * bx = goal_x
    # m * ay + n * by = goal_y
    
    determinant = (ax * by - bx * ay)
    
    if determinant == 0:
        return (0, 0) # No solution exists
        
    a_presses = (goal_x * by - bx * goal_y) / determinant
    b_presses = (ax * goal_y - goal_x * ay) / determinant

    if int(a_presses) != a_presses or int(b_presses) != b_presses:
        return (0, 0)  # No integer solution exists
    
    return (a_presses, b_presses)



def part_1(data: InputData) -> int:
    cost = 0
    for prize, a, b in data:
        a_presses, b_presses = find_steps_to_goal(a, b, prize)
        if 0 < a_presses <= 100 and 0 < b_presses <= 100:
            cost += (a_presses * 3) + b_presses

    return int(cost)


def part_2(data: InputData) -> int:
    prize_multiplier = 10000000000000
    cost = 0
    for prize, a, b in data:
        prize_coord  = (prize[0] + prize_multiplier, prize[1] + prize_multiplier)
        a_presses, b_presses = find_steps_to_goal(a, b, prize_coord)
        if 0 < a_presses and 0 < b_presses:
            cost += (a_presses * 3) + b_presses

    return int(cost)


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 30973

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer != 0
    assert part2_answer == 95688837203288


if __name__ == "__main__":
    main()
