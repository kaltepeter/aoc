from copy import deepcopy
import os
import re
from pathlib import Path
from typing import Generator, List


base_path = Path(__file__).parent

InputData = tuple[List[int], dict[str, List[tuple[int, int, int]]]]


def split_to_list_of_tuples(input: str) -> List[tuple[int, int, int]]:
    return list(
        map(
            lambda val: tuple(int(x) for x in val.strip().split()),
            input.strip().split("\n"),
        )
    )


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        seeds = []
        maps = {}
        lines = reader.read().split("\n\n")
        for line in lines:
            match line.split(":"):
                case ["seeds", nums]:
                    seeds = list(map(int, nums.strip().split()))
                case ["seed-to-soil map", nums]:
                    maps["seed_to_soil"] = split_to_list_of_tuples(nums)
                case ["soil-to-fertilizer map", nums]:
                    maps["soil_to_fertilizer"] = split_to_list_of_tuples(nums)
                case ["fertilizer-to-water map", nums]:
                    maps["fertilizer_to_water"] = split_to_list_of_tuples(nums)
                case ["water-to-light map", nums]:
                    maps["water_to_light"] = split_to_list_of_tuples(nums)
                case ["light-to-temperature map", nums]:
                    maps["light_to_temperature"] = split_to_list_of_tuples(nums)
                case ["temperature-to-humidity map", nums]:
                    maps["temperature_to_humidity"] = split_to_list_of_tuples(nums)
                case ["humidity-to-location map", nums]:
                    maps["humidity_to_location"] = split_to_list_of_tuples(nums)
                case _:
                    print("should not be here")

        return (seeds, maps)


def split_into_pairs(lst):
    pairs = []
    for i in range(0, len(lst), 2):
        pair = lst[i : i + 2]
        pairs.append(pair)
    return pairs


def part_1(data: InputData) -> int:
    seeds, maps = data
    for ranges in maps.values():
        locations = []

        for seed in seeds:
            for dest, source, span in ranges:
                if seed in range(source, source + span):
                    locations.append(seed - source + dest)
                    break
            else:
                locations.append(seed)
        seeds = locations

    return min(locations)


def part_2(data: InputData) -> int:
    seeds, maps = data
    seed_ranges = list(
        map(lambda val: (val[0], val[0] + val[1]), split_into_pairs(seeds))
    )
    for ranges in maps.values():
        locations = []

        while len(seed_ranges) > 0:
            start, end = seed_ranges.pop()
            for dest, source, span in ranges:
                o_start = max(start, source)
                o_end = min(end, source + span)
                if o_start < o_end:
                    locations.append((o_start - source + dest, o_end - source + dest))
                    if o_start > start:
                        seed_ranges.append((start, o_start))
                    if end > o_end:
                        seed_ranges.append((o_end, end))
                    break

            else:
                locations.append((start, end))
        seed_ranges = locations

    return min(min(locations))


def main():
    pi = list(process_input(os.path.join(base_path, "input.txt")))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 227653707

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 78775051


if __name__ == "__main__":
    main()
