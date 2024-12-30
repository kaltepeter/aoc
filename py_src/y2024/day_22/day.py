from copy import deepcopy
from functools import lru_cache
import os
from pathlib import Path
from typing import List
from tqdm import tqdm


base_path = Path(__file__).parent

InputData = List[int]
PriceMap = dict[tuple[int, int, int, int], int]


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        block = reader.read().split("\n\n")[0]
        return list(map(int, block.splitlines()))
    

def mix_number(secret_number: int, val: int) -> int:
    return secret_number ^ val


def prune_number(secret_number: int) -> int:
    return secret_number % 16777216


def get_next_secret_number(secret_number: int) -> int:
    step1 = secret_number * 64
    secret_number = prune_number(mix_number(secret_number, step1))
    step2 = secret_number // 32
    secret_number = prune_number(mix_number(secret_number, step2))
    step3 = secret_number * 2048
    secret_number = prune_number(mix_number(secret_number, step3))
    return secret_number


@lru_cache(None)
def get_x_secret_number(secret_number: int, iterations: int = 2000) -> tuple[int, List[int]]:
    results = [secret_number % 10]
    for i in range(iterations):
        secret_number = get_next_secret_number(secret_number)
        results.append(secret_number % 10)
    
    return (secret_number, results)


@lru_cache(None)
def get_x_secret_number_price_map(secret_number: int, iterations: int = 2000) -> tuple[int, PriceMap]:
    price_map:PriceMap = {}
    results = [secret_number % 10]
    for i in range(iterations):
        secret_number = get_next_secret_number(secret_number)
        results.append(secret_number % 10)

        if i >= 5:
            changes = tuple([results[j] - results[j - 1] for j in range(i-2, i+2)])
            if not changes in price_map:
                price_map[changes] = secret_number % 10
    
    return (secret_number, price_map)


def get_total_profit(secret_number: int, profits: List[PriceMap]) -> int:
    result = 0
    for profit in profits:
        if secret_number in profit:
            result += profit[secret_number]
            
    return result


def calculate_profits(data: InputData) -> List[PriceMap]:
    return [get_x_secret_number_price_map(secret_number)[1] for secret_number in data]


def part_1(data: InputData, iterations: int = 2000) -> int:
    result = 0
    for secret_number in data:
        result += get_x_secret_number(secret_number, iterations)[0]

    return result


def part_2(data: InputData) -> int:
    profits = calculate_profits(data)

    seqs = set()
    for profit in tqdm(profits):
        seqs = seqs.union(profit.keys())

    best = 0
    for seq in tqdm(seqs):
        best = max(best, get_total_profit(seq, profits))
         
    return best



def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 19927218456

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 2189


if __name__ == "__main__":
    main()
