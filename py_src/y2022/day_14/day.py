from copy import deepcopy
import os
from pathlib import Path
from typing import Generator, List, Tuple

from py_src.shared.graph import GridLocation


base_path = Path(__file__).parent


class ReservoirMap:
    def __init__(self):
        self.lowest_x: int = 0
        self.lowest_y: int = 0
        self.highest_x: int = 0
        self.highest_y: int = 0
        self.has_floor = False
        self.floor_y: int = 0
        self.rocks: set[GridLocation] = set()
        self.sand: set[GridLocation] = set()

    def in_bounds(self, location: GridLocation) -> bool:
        (x, y) = location
        if self.has_floor == True:
            return True

        return (
            self.lowest_x <= x < self.highest_x and self.lowest_y <= y < self.highest_y
        )

    def is_floor(self, location: GridLocation) -> bool:
        (x, y) = location
        return y == self.floor_y

    def passable(self, location: GridLocation) -> bool:
        return (
            location not in self.rocks
            and location not in self.sand
            and not self.is_floor(location)
        )

    def add_rock(self, location: GridLocation) -> None:
        (x, y) = location
        if x < self.lowest_x:
            self.lowest_x = x
        if x > self.highest_x:
            self.highest_x = x
        if y < self.lowest_y:
            self.lowest_y = y
        if y > self.highest_y:
            self.highest_y = y

        self.rocks.add(location)

    def add_sand(self, location: GridLocation) -> None:
        (x, y) = location
        if x < self.lowest_x:
            self.lowest_x = x
        if x > self.highest_x:
            self.highest_x = x
        if y < self.lowest_y:
            self.lowest_y = y
        if y > self.highest_y:
            self.highest_y = y

        self.sand.add(location)

    def move_sand(
        self, location: GridLocation, path_list: List[GridLocation]
    ) -> Generator[Tuple[GridLocation, List[GridLocation]], None, None]:
        (x, y) = location
        path = [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]
        results = list(filter(self.passable, path))
        if len(results) == 0:
            self.add_sand(location)
            yield (
                location,
                path_list,
            )

        new_loc = results[0]
        if (
            self.in_bounds(new_loc)
            and self.passable(new_loc)
            and not self.is_floor(new_loc)
        ):
            path_list.append(new_loc)
            yield from self.move_sand(new_loc, path_list)

        yield (
            new_loc,
            path_list,
        )


SAND_START: GridLocation = (500, 0)
START_CHAR = "+"
SAND_CHAR = "o"
ROCK_CHAR = "#"
EMPTY_SPACE_CHAR = "."
InputData = ReservoirMap


def get_printable_map(
    data: InputData,
) -> Generator[str, None, None]:
    graph = data

    for y in range(data.lowest_y, data.highest_y + 3):
        for x in range(data.lowest_x, data.highest_x + 1):
            location = (x, y)
            if location == SAND_START:
                yield START_CHAR
            elif location in graph.rocks or graph.is_floor(location):
                yield ROCK_CHAR
            elif location in graph.sand:
                yield SAND_CHAR
            else:
                yield EMPTY_SPACE_CHAR
        yield "\n"


def print_reservoir_map(data: InputData):
    for i in get_printable_map(
        data,
    ):
        print(i, end="")
    return data


def str_loc_to_location(val: str) -> GridLocation:
    if len(val) < 1:
        return
    return tuple(map(lambda val: int(val), val.split(",")))


def process_input(file: str) -> InputData:
    reservoir_map = ReservoirMap()
    reservoir_map.lowest_x = SAND_START[0]
    reservoir_map.highest_x = SAND_START[0]
    reservoir_map.lowest_y = SAND_START[1]
    reservoir_map.highest_y = SAND_START[1]
    with open(file, "r") as reader:
        for line in reader.read().split("\n"):
            coords = list(
                map(
                    str_loc_to_location,
                    line.strip().split(" -> "),
                )
            )
            for c in range(0, len(coords) - 1):
                x, y = coords[c]
                to_x, to_y = coords[c + 1]
                if x == to_x:
                    # vertical
                    r_vals = sorted([y, to_y])
                    for new_y in range(r_vals[0], r_vals[1] + 1):
                        val = (x, new_y)
                        reservoir_map.add_rock(val)
                elif y == to_y:
                    # horizontal
                    r_vals = sorted([x, to_x])
                    for new_x in range(r_vals[0], r_vals[1] + 1):
                        val = (new_x, y)
                        reservoir_map.add_rock(val)
                else:
                    raise Exception("Invalid input")

        return reservoir_map


def part_1(data: InputData) -> int:
    run_simulation = True
    count = 0
    sand = SAND_START
    path_list = list()
    while run_simulation == True:
        nl = data.move_sand(sand, path_list)
        new_location, pl = next(nl)
        if data.in_bounds(new_location) == False:
            run_simulation = False
        else:
            count += 1

    # print_reservoir_map(data)
    # print()
    return count


def part_2(data: InputData) -> int:
    data.has_floor = True
    data.floor_y = data.highest_y + 2

    sand = SAND_START

    nl = data.move_sand(sand, list())
    new_location, pl = next(nl)
    count = 1

    while new_location != SAND_START:
        if pl[-1] in data.sand:
            pl.pop()

        start_location = pl[-1] if len(pl) > 0 else SAND_START

        nl = data.move_sand(start_location, pl)
        new_location, pl = next(nl)

        count += 1

    # print_reservoir_map(data)
    # print()

    return count


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 737

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 28145


if __name__ == "__main__":
    main()
