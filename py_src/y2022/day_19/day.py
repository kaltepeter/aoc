from copy import deepcopy
import os
from pathlib import Path
from typing import List
import re
from functools import reduce

base_path = Path(__file__).parent

Cost = tuple[int, int, int]  # ore, clay, obsidian
BluePrint = dict[str, Cost]
InputData = dict[int, BluePrint]
Spends = dict[int, List[int]]

bot_types = {
    "ore": 0,
    "clay": 1,
    "obsidian": 2,
    "geode": 3,
}


def process_input(file: str) -> InputData:
    blueprints = {}
    with open(file, "r") as reader:
        for line in reader.read().splitlines():
            m = re.match(
                r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.",
                line,
            )
            m = map(int, m.groups())
            name, *costs = m
            blueprints[name] = {
                "ore": (costs[0], 0, 0),
                "clay": (costs[1], 0, 0),
                "obsidian": (costs[2], costs[3], 0),
                "geode": (costs[4], 0, costs[5]),
            }
    return blueprints


def process_blueprint(
    id: int,
    bp: BluePrint,
    max_spend: dict[str, int],
    cache: dict[str, int],
    time: int,
    robots: Cost,
    amount: List[int],
) -> int:
    if time == 0:
        return amount[3]

    key = tuple([time, *robots, *amount])

    if key in cache:
        return cache[key]

    max_val = amount[3] + robots[3] * time

    for btype, recipe in bp.items():
        bot_type = bot_types[btype]
        if bot_type != 3 and robots[bot_type] >= max_spend[id][bot_type]:
            continue

        wait = 0
        for resource_type, resource_amount in enumerate(recipe):
            if resource_amount == 0:
                continue

            if robots[resource_type] == 0:
                break

            wait = max(
                wait,
                -(-(resource_amount - amount[resource_type]) // robots[resource_type]),
            )
        else:
            remaining_time = time - wait - 1
            if remaining_time <= 0:
                continue
            robots_ = robots[:]
            amount_ = [x + y * (wait + 1) for x, y in zip(amount, robots)]
            for resource_type, resource_amount in enumerate(recipe):
                if resource_amount == 0:
                    continue

                amount_[resource_type] -= resource_amount

            robots_[bot_type] += 1

            for i in range(3):
                amount_[i] = min(amount_[i], max_spend[id][i] * remaining_time)

            max_val = max(
                max_val,
                process_blueprint(
                    id, bp, max_spend, cache, remaining_time, robots_, amount_
                ),
            )

    cache[key] = max_val
    return max_val


def calculate_max_spends(data: InputData) -> Spends:
    max_spend: Spends = {}
    for id, bp in data.items():
        if id not in max_spend:
            max_spend[id] = [0, 0, 0]

        for val in bp.values():
            max_spend[id][0] = max(max_spend[id][0], val[0])
            max_spend[id][1] = max(max_spend[id][1], val[1])
            max_spend[id][2] = max(max_spend[id][2], val[2])

    return max_spend


def part_1(data: InputData, max_spend: Spends) -> int:
    quality_levels = []

    for id, bp in data.items():
        robots = [1, 0, 0, 0]  # ore, clay, obsidian, geode
        geode_count = process_blueprint(id, bp, max_spend, {}, 24, robots, [0, 0, 0, 0])
        quality_levels.append(geode_count * (id))

    return sum(quality_levels)


def part_2(data: InputData, max_spend: Spends) -> int:
    geode_counts = []

    for id, bp in list(data.items())[:3]:
        robots = [1, 0, 0, 0]  # ore, clay, obsidian, geode
        geode_count = process_blueprint(id, bp, max_spend, {}, 32, robots, [0, 0, 0, 0])
        geode_counts.append(geode_count)

    return reduce(lambda x, y: x * y, geode_counts)


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))
    max_spend = calculate_max_spends(pi)

    part1_answer = part_1(deepcopy(pi), max_spend)
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 1650

    part2_answer = part_2(deepcopy(pi), max_spend)
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 5824


if __name__ == "__main__":
    main()
