from copy import deepcopy
import os
from pathlib import Path
from typing import List
from collections import defaultdict, deque


base_path = Path(__file__).parent

PageList = List[int]
RuleList = List[tuple[int, int]]
Rule = List[int]
RuleMap = dict[int, Rule]

InputData = tuple[RuleList, List[PageList]]


def process_input(file: str) -> InputData:
    with open(file, "r") as reader:
        rule_block, page_block = reader.read().split("\n\n")
        rules = list(map(lambda val: tuple(map(int, val.split('|'))), rule_block.splitlines()))
        page_list = list(map(lambda val: list(map(int, val.split(','))), page_block.splitlines()))
        return (rules, page_list)

def calc_valid_pages(valid_page_lists: List[PageList]) -> int:
    total = 0
    for page_list in valid_page_lists:
        if len(page_list) % 2 == 0:
            raise ValueError("Page list must have an odd number of pages")
        
        total += page_list[len(page_list) // 2]

    return total

def process_rules(rule_list: RuleList) -> RuleMap:
    rule_map = {}

    for left, right in rule_list:
        if left not in rule_map:
            rule_map[left] = [right]
        else:
            rule_map[left].append(right)

    return rule_map

def find_common_numbers(array1, array2):
    return list(set(array1) & set(array2))

def find_valid_and_invalid_page_lists(rule_map: RuleMap, page_lists: List[PageList]) -> tuple[List[PageList], List[PageList]]:
    valid_page_lists = []
    invalid_page_lists = []

    for page_list in page_lists:
        is_valid = True
        for page in page_list:
            if not is_valid:
                break

            if page in rule_map: 
                to_check = find_common_numbers(page_list, rule_map[page])
                for check in to_check:
                    left_index = page_list.index(page)
                    right_index = page_list.index(check)
                    if left_index > right_index:
                        is_valid = False
                        break

        if is_valid:
            valid_page_lists.append(page_list)
        else:
            invalid_page_lists.append(page_list)

    return (valid_page_lists, invalid_page_lists)


def fix_list(rule_map: RuleMap, page_list: PageList) -> PageList:
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    
    # Build graph from rules that apply to pages in page_list
    for page in page_list:
        if page in rule_map:
            for dependent in rule_map[page]:
                if dependent in page_list:
                    graph[page].append(dependent)
                    in_degree[dependent] += 1
    
    # Initialize queue with nodes having no dependencies
    queue = deque([page for page in page_list if in_degree[page] == 0])
    result = []
    
    # Perform topological sort
    while queue:
        current = queue.popleft()
        result.append(current)
        
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # If result length matches input length, we have a valid ordering
    if len(result) == len(page_list):
        return result
    
    return [] 



def part_1(data: InputData) -> int:
    (rules, page_lists) = data
    rule_map = process_rules(rules)

    (valid_page_lists, _) = find_valid_and_invalid_page_lists(rule_map, page_lists)

    return calc_valid_pages(valid_page_lists)


def part_2(data: InputData) -> int:
    (rules, page_lists) = data
    rule_map = process_rules(rules)

    final_lists = []

    (_, invalid_page_lists) = find_valid_and_invalid_page_lists(rule_map, page_lists)

    for invalid_list in invalid_page_lists:
        fixed_list = fix_list(rule_map, invalid_list)
        if fixed_list:
            final_lists.append(fixed_list)

    return calc_valid_pages(final_lists)


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 5588

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 5331


if __name__ == "__main__":
    main()
