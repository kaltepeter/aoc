from copy import deepcopy
import os
from pathlib import Path
from typing import Generator, List


base_path = Path(__file__).parent

InputData = List[str]


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        for blocks in reader.read().split("\n\n"):
            return list(map(lambda val: val.strip(), blocks.splitlines()))

def search_word_2d(grid: List[str], row: int, col: int, word: str) -> int:
    m = len(grid)
    n = len(grid[0])

    if grid[row][col] != word[0]:
        return False
    
    len_word = len(word)

    x = [-1, -1, -1, 0, 0, 1, 1, 1]
    y = [-1, 0, 1, -1, 1, -1, 0, 1]
    count = 0

    for dir in range(8):
        cur_x, cur_y = row + x[dir], col + y[dir]
        k = 1

        while k < len_word:
            if cur_x >= m or cur_x < 0 or cur_y >= n or cur_y < 0:
                break

            if grid[cur_x][cur_y] != word[k]:
                break

            cur_x += x[dir]
            cur_y += y[dir]
            k += 1

        if k == len_word:
            count += 1
        
    return count

def part_1(grid: InputData) -> int:
    chars = "XMAS"

    m = len(grid)
    n = len(grid[0])

    ans = []
    total = 0

    for i in range(m):
        for j in range(n):
            count = search_word_2d(grid, i, j, chars)
            if count > 0:
                ans.append(((i, j), count))
                total += count

    return total


def part_2(data: InputData) -> int:
    return 0


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 2639

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
