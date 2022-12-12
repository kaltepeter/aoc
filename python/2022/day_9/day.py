import os
from pathlib import Path
from typing import List, Literal, Set, Tuple
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


base_path = Path(__file__).parent

Position = Tuple[int, int]
Dir = Literal["U", "D", "L", "R"]
Move = Tuple[Dir, int]
Moves = List[Move]
Rope = List[Position]


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
        # print(f"move: {m} h:{h} t:{t}")
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


def plot_rope(rope: Rope) -> None:
    # rope.reverse()
    fig, ax = plt.subplots()
    minX, maxX = min(rope)[0], max(rope)[0]
    minY, maxY = min(rope)[1], max(rope)[1]

    ax.set(xlim=(minX, maxX), ylim=(minY, maxY))

    Path = mpath.Path
    path_data = [(Path.MOVETO, rope[0])]
    for knot in rope[1:]:
        # path_data.append((Path.MOVETO, knot))
        path_data.append((Path.LINETO, knot))

    codes, verts = zip(*path_data)
    path = mpath.Path(verts, codes)
    patch = mpatches.PathPatch(path, fill=False, joinstyle="round", capstyle="round")
    ax.set_anchor("C")
    ax.add_patch(patch)

    # plot control points and connecting lines
    x, y = zip(*path.vertices)
    (line,) = ax.plot(x, y, "go-")

    ax.grid()
    ax.axis("equal")
    plt.show()


def move_knot(
    knot: int, prev_knot: int, m: Move, rope: Rope, visited: Set[Position] = set()
) -> Tuple[Rope, Set[Position]]:
    knot_pos = rope[knot]
    # if knot is not touching previous know and row and col do not match move diagonally
    if (
        knot_pos[0] != rope[prev_knot][0]
        and knot_pos[1] != rope[prev_knot][1]
        and not is_touching(rope[prev_knot], rope[knot])
    ):
        rope[knot] = get_diag(rope[prev_knot], rope[knot])[0]
    # if knot is not touching previous know move in direction of move
    if not is_touching(rope[prev_knot], rope[knot]):
        rope[knot] = move(rope[knot], (m[0], 1))

    for k in range(knot + 1, len(rope)):
        if not is_touching(rope[k - 1], rope[k]):
            rope, v = move_knot(k, k - 1, m, rope, visited)
            visited.update(v)
        else:
            # print(f"k: {k} m: {m} rope: {rope}")
            break

    visited.add(rope[-1])

    # if knot is not touching previous know raise error
    #  catch error
    # if not is_touching(rope[prev_knot], rope[knot]):
    #     print(rope)
    #     raise ValueError(f"Too far away: knot: {knot} prev_knot: {prev_knot}")

    return (rope, visited)


def part_2(moves: Moves) -> int:
    s = (0, 0)
    visited = set()
    visited.add(s)
    rope: Rope = [s for _ in range(10)]
    for idx, m in enumerate(moves):
        print(f"move: {m} h:{rope[0]} t:{rope[-1]} ")
        for i in range(m[1]):
            # move head
            rope[0] = move(rope[0], (m[0], 1))

            # loop through knots in rope H+1 -- T
            for knot, knot_pos in enumerate(rope):
                # skip head
                if knot == 0:
                    continue

                prev_knot = knot - 1
                # if knot touches prev knot move on
                if is_touching(rope[prev_knot], rope[knot]):
                    continue

                # print(
                #     f"\ti: {i} knot: {knot} knot_pos: {knot_pos} prev_knot: {prev_knot} prev_knot_pos: {rope[prev_knot]}"
                # )

                rope, v = move_knot(knot, prev_knot, m, rope)
                visited.update(v)

            # visited.add(rope[-1])

    # plot_rope(rope)
    # print(f"\thead: {rope[0]} tail: {rope[-1]} rope: {rope} visited: {visited}")
    # print()

    return len(visited)


def main():
    moves = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(moves)
    print(f"Part I: {part1_answer} spaces visited")
    assert part1_answer == 6023

    part2_answer = part_2(moves)
    print(f"Part II: {part2_answer} spaces visited")
    assert part2_answer > 2532 and part2_answer < 2601


if __name__ == "__main__":
    main()
