import copy
import os
from pathlib import Path
from typing import List, Set, Tuple


base_path = Path(__file__).parent

TreeRow = List[int]
TreeGrid = List[TreeRow]
VisibleTrees = List[Tuple[int, int]]  # y,x


def process_input(file: str) -> TreeGrid:
    tree_grid = []
    with open(file) as reader:
        rows = reader.read().strip().split("\n")
        for row in rows:
            tree_grid.append([int(x) for x in [*row]])
    return tree_grid


def get_indexes_to_check(
    rowLength: int, colLength: int, coord: Tuple[int, int]
) -> Set[Tuple[int, int]]:
    rowIdx, colIdx = coord
    coords = set()

    leftIndexes = [x for x in range(0, colIdx)]
    rightIndexes = [x for x in range(colIdx, colLength)]
    upIndexes = [y for y in range(0, rowIdx)]
    downIndexes = [y for y in range(rowIdx, rowLength)]
    xIndexes = [(x, colIdx) for x in leftIndexes + rightIndexes]
    yIndexes = [(rowIdx, y) for y in upIndexes + downIndexes]
    coords |= set(xIndexes)
    coords |= set(yIndexes)
    coords.remove(coord)

    return coords


def is_visible(row: TreeRow, colIdx: int) -> bool:
    col = row[colIdx]
    left_range = list(range(0, colIdx))
    left_range.sort(reverse=True)

    right_range = list(range(colIdx + 1, len(row)))

    # print(f"col: {col}, colIdx: {colIdx} rr: {right_range} lr: {left_range}")
    if colIdx == 0 or colIdx == len(row) - 1:
        return True

    left_visible = False
    right_visible = False
    for y in left_range:
        # print(f"left: {y} {row[y] < col}")
        if row[y] < col:
            left_visible = True
        else:
            left_visible = False
            break

    for y in right_range:
        # print(f"right: {y} {row[y] < col}")
        if row[y] < col:
            right_visible = True
        else:
            right_visible = False
            break

    return left_visible or right_visible


def part_1(trees: TreeGrid) -> int:
    trees_to_check = copy.copy(trees)
    visible_trees = []
    for rowIdx in range(len(trees_to_check)):
        row = trees_to_check[rowIdx]
        for colIdx in range(len(row)):
            if rowIdx == 0 or rowIdx == len(trees_to_check) - 1:
                visible_trees.append((rowIdx, colIdx))
            elif colIdx == 0 or colIdx == len(row) - 1:
                visible_trees.append((rowIdx, colIdx))
            else:
                col = row[colIdx]

                vertical_slice = [
                    trees_to_check[x][colIdx] for x in range(0, len(trees_to_check))
                ]

                y_found = is_visible(row, colIdx)
                if y_found:
                    visible_trees.append((rowIdx, colIdx))
                    continue

                x_found = is_visible(vertical_slice, rowIdx)
                if x_found:
                    visible_trees.append((rowIdx, colIdx))
                    continue

    return len(visible_trees)


def part_2(trees: TreeGrid) -> int:
    return 0


def main():
    file_tree = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(file_tree)
    print(f"Part I: {part1_answer} trees are visible")
    assert part1_answer == 1776

    part2_answer = part_2(file_tree)
    print(f"Part II: {part2_answer} trees are visible")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
