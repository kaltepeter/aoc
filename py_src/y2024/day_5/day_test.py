import os
from pathlib import Path

import pytest
from .day import calc_valid_pages, find_common_numbers, fix_list, part_1, part_2, process_input, process_rules, PageList, RuleMap

base_path = Path(__file__).parent


@pytest.fixture()
def example_data():
    return process_input(os.path.join(base_path, "example.txt"))

@pytest.fixture()
def rule_map(example_data):
    return process_rules(example_data[0])


def test_process_input(example_data):
    (rules, page_list) = example_data
    assert len(rules) == 21
    assert rules[0] == (47, 53)

    assert len(page_list) == 6
    assert page_list[0] == [75, 47, 61, 53, 29]


def test_calc_valid_pages():
    valid_page_list = [[75, 47, 61, 53, 29], [97, 61, 53, 29, 13], [75, 29, 13]]
    assert calc_valid_pages(valid_page_list) == 143


def test_calc_valid_pages_even_list_error():
    valid_page_list = [[75, 47, 61, 53], [97, 61, 53, 29, 13], [75, 29, 13]]
    with pytest.raises(ValueError):
        assert calc_valid_pages(valid_page_list)


def test_process_rules():
    rules = [(47, 53), (97, 13), (97, 61), (97, 47)]
    expected_map = {
        47:  [53],
        97: [13, 61, 47]
    }
    assert process_rules(rules) == expected_map

def test_find_common_numbers():
    list_1 = [1, 2, 3, 4, 5]
    list_2 = [2, 3, 4, 5, 6]
    assert find_common_numbers(list_1, list_2) == [2, 3, 4, 5]

@pytest.mark.parametrize(
        'invalid, expected',
        [
            ([75,97,47,61,53], [97,75,47,61,53]),
            ([61,13,29], [61,29,13]),
            ([97,13,75,29,47], [97,75,47,29,13])
        ]
)
def test_fix_list(rule_map: RuleMap, invalid: PageList, expected: PageList):
    assert fix_list(rule_map, invalid) == expected


def test_part_1(example_data):
    assert part_1(example_data) == 143


def test_part_2(example_data):
    assert part_2(example_data) == 123
