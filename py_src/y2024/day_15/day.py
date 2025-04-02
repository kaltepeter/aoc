from copy import deepcopy
import os
from pathlib import Path
from typing import List

from py_src.shared.graph import SquareGrid, GridLocation


base_path = Path(__file__).parent

direction = {
    "<": (-1, 0),
    ">": (1, 0),
    "^": (0, -1),
    "v": (0, 1),
}


class Warehouse(SquareGrid):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.start: GridLocation = None
        self.boxes: list[GridLocation] = []

    def get_gps(self, coord: GridLocation) -> int:
        return (100 * coord[1]) + coord[0]

    def move_boxes(self, move: str) -> None:
        x, y = self.start
        dx, dy = direction[move]
        new_pos = (x + dx, y + dy)

        boxes_to_check = [
            box
            for box in self.boxes
            if (dx != 0 and box[1] == y) or (dy != 0 and box[0] == x)
        ]
        new_boxes = [box for box in self.boxes if box not in boxes_to_check]
        while new_pos in boxes_to_check:
            boxes_to_check.remove(new_pos)
            new_pos = (new_pos[0] + dx, new_pos[1] + dy)
            if not self.passable(new_pos):
                return

            new_boxes.append(new_pos)

        self.boxes = new_boxes + boxes_to_check

    def move(self, move: str) -> GridLocation:
        x, y = self.start
        dx, dy = direction[move]
        new_pos = (x + dx, y + dy)
        if not self.passable(new_pos):
            return self.start

        if new_pos in self.boxes:
            self.move_boxes(move)

        if new_pos in self.boxes:
            return self.start
        else:
            self.start = new_pos
            return new_pos


def sort_boxes(boxes: List[GridLocation]) -> List[GridLocation]:
    return sorted(boxes, key=lambda x: (x[1], x[0]))


class LargeWarehouse(Warehouse):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)


    def move_boxes(self, move: str) -> bool:
        x, y = self.start
        dx, dy = direction[move]
        new_x, new_y = x + dx, y + dy

        if not self.in_bounds((new_x, new_y)):
            return

        if (new_x, new_y) in self.walls:
            return

        stack = []
        if (new_x, new_y) in self.boxes:
            stack.append((new_x, new_y))
        
        if (new_x - 1, new_y) in self.boxes:
            stack.append((new_x - 1, new_y))

        can_move = True

        seen = set()
        while len(stack) > 0:
            topx, topy = stack.pop()
            nx, ny = topx + dx, topy + dy

            if not self.in_bounds((nx, ny)):
                can_move = False
                break

            if (nx, ny) in self.walls or (nx + 1, ny) in self.walls:
                can_move = False
                break

            if (topx, topy) in seen:
                continue

            seen.add((topx, topy))

            if (nx, ny) in self.boxes:
                stack.append((nx, ny))
            if (nx - 1, ny) in self.boxes:
                stack.append((nx - 1, ny))
            if (nx + 1, ny) in self.boxes:
                stack.append((nx + 1, ny))

        if can_move:
            for i, box in enumerate(self.boxes):
                if box in seen:
                    self.boxes[i] = (box[0] + dx, box[1] + dy)

        return can_move


    def move(self, move: str) -> GridLocation:
        x, y = self.start
        dx, dy = direction[move]
        new_pos = (x + dx, y + dy)
        # if not self.passable(new_pos):
        #     return self.start

        can_move = self.move_boxes(move)

        if not can_move:
            return self.start
        else:
            self.start = new_pos
            return new_pos


InputData = tuple[Warehouse, List[str]]
InputDataPart2 = tuple[LargeWarehouse, List[str]]


def print_warehouse(warehouse: LargeWarehouse) -> None:
    box_starts = [pos for pos in warehouse.boxes]
    box_ends = [(x + 1, y) for x, y in box_starts]
    for y in range(warehouse.height):
        for x in range(warehouse.width):
            if (x, y) == warehouse.start:
                print("@", end="")
            elif (x, y) in box_starts:
                print("[", end="")
            elif (x, y) in box_ends:
                print("]", end="")
            elif (x, y) in warehouse.walls:
                print("#", end="")
            else:
                print(".", end="")
        print()


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        g, m = reader.read().split("\n\n")
        grid = g.splitlines()
        warehouse = Warehouse(len(grid[0]), len(grid))
        for y, row in enumerate(grid):
            for x, char in enumerate(row):
                if char == "#":
                    warehouse.walls.append((x, y))
                elif char == "O":
                    warehouse.boxes.append((x, y))
                elif char == "@":
                    warehouse.start = (x, y)

        moves = m.replace("\n", "")

        return (warehouse, moves)


def process_input_large_warehouse(file: str) -> InputDataPart2:
    with open(file, "r") as reader:
        g, m = reader.read().split("\n\n")
        grid = g.splitlines()
        warehouse = LargeWarehouse(len(grid[0]) * 2, len(grid))
        for y, row in enumerate(grid):
            large_row = (
                row.replace("#", "##")
                .replace(".", "..")
                .replace("O", "[]")
                .replace("@", "@.")
            )
            for x, char in enumerate(large_row):
                if char == "#":
                    warehouse.walls.append((x, y))
                elif char == "[":
                    warehouse.boxes.append((x, y))
                elif char == "@":
                    warehouse.start = (x, y)

        moves = m.replace("\n", "")

        return (warehouse, moves)


def part_1(data: InputData) -> int:
    warehouse, moves = data
    for move in moves:
        warehouse.move(move)
        # print(f"Move: {i} {move}")
        # print_warehouse(warehouse)
        # print()

    return sum(warehouse.get_gps(x) for x in warehouse.boxes)


def part_2(data: InputData) -> int:
    warehouse, moves = data
    for move in moves:
        # print(f"Move: {i} {move}")
        warehouse.move(move)
        # print_warehouse(warehouse)
        # print()

    return sum(warehouse.get_gps(x) for x in warehouse.boxes)


def main():
    data = os.path.join(base_path, "input.txt")
    pi = process_input(data)

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 1517819


    pi2 = process_input_large_warehouse(data)
    part2_answer = part_2(deepcopy(pi2))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer > 1517819
    assert part2_answer == 1538862


if __name__ == "__main__":
    main()
