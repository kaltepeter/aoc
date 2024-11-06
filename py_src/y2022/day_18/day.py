from copy import deepcopy
import os
from pathlib import Path
from typing import Generator, List
from collections import deque

base_path = Path(__file__).parent

Location = tuple[int, int, int]
InputData = List[Location]


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        for blocks in reader.read().split("\n\n"):
            return list(
                map(
                    lambda val: tuple(map(int, val.strip().split(","))),
                    blocks.splitlines(),
                )
            )


def part_1(data: InputData) -> int:
    faces = {}
    offsets = [
        (0.5, 0, 0),
        (0, 0.5, 0),
        (0, 0, 0.5),
        (-0.5, 0, 0),
        (0, -0.5, 0),
        (0, 0, -0.5),
    ]
    for x, y, z in data:
        for dx, dy, dz in offsets:
            key = (x + dx, y + dy, z + dz)
            if key not in faces:
                faces[key] = 0
            faces[key] += 1

    return list(faces.values()).count(1)


def part_2(data: InputData) -> int:
    faces = {}
    offsets = [
        (0.5, 0, 0),
        (0, 0.5, 0),
        (0, 0, 0.5),
        (-0.5, 0, 0),
        (0, -0.5, 0),
        (0, 0, -0.5),
    ]

    min_x = min_y = min_z = float("inf")
    max_x = max_y = max_z = -float("inf")

    droplet = set()

    for x, y, z in data:
        droplet.add((x, y, z))
        min_x, min_y, min_z = min(min_x, x), min(min_y, y), min(min_z, z)
        max_x, max_y, max_z = max(max_x, x), max(max_y, y), max(max_z, z)

        for dx, dy, dz in offsets:
            key = (x + dx, y + dy, z + dz)
            if key not in faces:
                faces[key] = 0
            faces[key] += 1

    min_x -= 1
    min_y -= 1
    min_z -= 1

    max_x += 1
    max_y += 1
    max_z += 1

    q = deque([(min_x, min_y, min_z)])
    air = {(min_x, min_y, min_z)}

    while q:
        x, y, z = q.popleft()

        for dx, dy, dz in offsets:
            nx, ny, nz = key = (x + dx * 2, y + dy * 2, z + dz * 2)

            if not (
                min_x <= nx <= max_x and min_y <= ny <= max_y and min_z <= nz <= max_z
            ):
                continue

            if key in droplet or key in air:
                continue

            air.add(key)
            q.append(key)

    free = set()
    for x, y, z in air:
        for dx, dy, dz in offsets:
            free.add((x + dx, y + dy, z + dz))

    return len(set(faces) & free)


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 4282

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 2452


if __name__ == "__main__":
    main()
