import os
from pathlib import Path

import dpath

from .day import (
    FileTree,
    NodeType,
    calc_all_dir_sizes,
    calc_dir_size,
    get_node_name,
    process_input,
    part_1,
    part_2,
    update_size_map,
)

base_path = Path(__file__).parent

example_file_tree = {
    "root": {
        "name": "root",
        "size": 0,
        "type": NodeType.D,
        "children": {
            "a": {
                "name": "a",
                "size": 0,
                "type": NodeType.D,
                "children": {
                    "e": {
                        "name": "e",
                        "size": 0,
                        "type": NodeType.D,
                        "children": {
                            "i": {
                                "name": "i",
                                "size": 584,
                                "type": NodeType.F,
                                "children": {},
                            },
                        },
                    },
                    "f": {
                        "name": "f",
                        "size": 29116,
                        "type": NodeType.F,
                        "children": {},
                    },
                    "g": {
                        "name": "g",
                        "size": 2557,
                        "type": NodeType.F,
                        "children": {},
                    },
                    "h.lst": {
                        "name": "h.lst",
                        "size": 62596,
                        "type": NodeType.F,
                        "children": {},
                    },
                },
            },
            "b.txt": {
                "name": "b.txt",
                "size": 14848514,
                "type": NodeType.F,
                "children": {},
            },
            "c.dat": {
                "name": "c.dat",
                "size": 8504156,
                "type": NodeType.F,
                "children": {},
            },
            "d": {
                "name": "d",
                "size": 0,
                "type": NodeType.D,
                "children": {
                    "j": {
                        "name": "j",
                        "size": 4060174,
                        "type": NodeType.F,
                        "children": {},
                    },
                    "d.log": {
                        "name": "d.log",
                        "size": 8033020,
                        "type": NodeType.F,
                        "children": {},
                    },
                    "d.ext": {
                        "name": "d.ext",
                        "size": 5626152,
                        "type": NodeType.F,
                        "children": {},
                    },
                    "k": {
                        "name": "k",
                        "size": 7214296,
                        "type": NodeType.F,
                        "children": {},
                    },
                },
            },
        },
    }
}


def test_calc_dir_size():
    aNode = dpath.get(example_file_tree, "root/children/a")
    dNode = dpath.get(example_file_tree, "root/children/d")
    assert calc_dir_size(aNode) == 94853
    assert calc_dir_size(dNode) == 24933642
    assert calc_dir_size(example_file_tree["root"]) == 48381165


def test_calc_all_dir_sizes():
    sm = {("root",): (0, NodeType.D)}
    assert calc_all_dir_sizes(example_file_tree, ["root"], sm) == {
        ("root", "a"): (94853, NodeType.D),
        ("root", "a", "e"): (584, NodeType.D),
        ("root", "a", "e", "i"): (584, NodeType.F),
        ("root", "a", "f"): (29116, NodeType.F),
        ("root", "a", "g"): (2557, NodeType.F),
        ("root", "a", "h.lst"): (62596, NodeType.F),
        ("root", "b.txt"): (14848514, NodeType.F),
        ("root", "c.dat"): (8504156, NodeType.F),
        ("root", "d"): (24933642, NodeType.D),
        ("root", "d", "j"): (4060174, NodeType.F),
        ("root", "d", "d.log"): (8033020, NodeType.F),
        ("root", "d", "d.ext"): (5626152, NodeType.F),
        ("root", "d", "k"): (7214296, NodeType.F),
        ("root",): (48381165, NodeType.D),
    }


def test_update_size_map():
    starting_map = {
        ("root", "bntdgzs"): (0, NodeType.D),
        ("root", "cjw.jgc"): (179593, NodeType.F),
        ("root", "grbwdwsm.znn"): (110209, NodeType.F),
        ("root",): (289802, NodeType.D),
    }
    expected_map = {
        ("root", "bntdgzs", "gcwcp"): (297955, NodeType.F),
        ("root", "bntdgzs"): (297955, NodeType.D),
        ("root", "cjw.jgc"): (179593, NodeType.F),
        ("root", "grbwdwsm.znn"): (110209, NodeType.F),
        ("root",): (587757, NodeType.D),
    }
    assert (
        update_size_map(
            ("root", "bntdgzs", "gcwcp"), (297955, NodeType.F), starting_map
        )
        == expected_map
    )


def test_get_node_name():
    assert get_node_name("/") == "root"
    assert get_node_name("a") == "a"


def test_process_input():
    assert process_input(os.path.join(base_path, "example.txt")) == example_file_tree


def test_part_1():
    file_tree = process_input(os.path.join(base_path, "example.txt"))
    assert part_1(file_tree) == 95437


def test_part_2():
    file_tree = process_input(os.path.join(base_path, "example.txt"))
    assert part_2(file_tree) == 0
