import copy
from enum import Enum
import os
from pathlib import Path
import re
from typing import Dict, List, Literal, Tuple, TypedDict

import dpath


base_path = Path(__file__).parent


class NodeType(Enum):
    F = "FILE"
    D = "DIR"


Node = TypedDict(
    "Node", {"name": str, "size": int, "type": NodeType, "children": Dict[str, "Node"]}
)
FileTree = Dict[str, Node]
SizeMap = Dict[Tuple[str, ...], Tuple[int, NodeType]]

# prefix components:
space = "    "
branch = "│   "
# pointers:
tee = "├── "
last = "└── "


def pretty_print_tree(tree: FileTree, indent: int = 0):
    for key, node in tree.items():
        info = f"(dir)"
        if node["type"] == NodeType.F:
            info = f"(file, size={node['size']})"

        print(" " * indent, key, info)
        pretty_print_tree(node["children"], indent + 4)


def get_tree(tree: FileTree, prefix: str = "", dir_size: int = 0):
    contents = list(tree.items())
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, (key, node) in zip(pointers, contents):
        info = f" (dir, size={dir_size})"
        if node["type"] == NodeType.F:
            dir_size += node["size"]
            info = f" (file, size={node['size']})"

        yield prefix + pointer + key + info
        if node["type"] == NodeType.D:
            extension = branch if pointer == tee else space
            yield from get_tree(
                node["children"], prefix=prefix + extension, dir_size=dir_size
            )


def is_root_node(name: str) -> bool:
    return name == "/"


def get_node_name(name: str) -> str:
    if is_root_node(name):
        return "root"
    else:
        return name


def calc_dir_size(node: FileTree) -> int:
    size = node["size"]
    startNode = node
    if "root" in node:
        startNode = node["root"]
    for child in startNode["children"].values():

        if child["type"] == NodeType.F:
            size += child["size"]
        else:
            size += calc_dir_size(child)
    return size


def calc_root_size(node: FileTree) -> int:
    size = 0
    startNode = node
    if "root" in node:
        startNode = node["root"]
    for child in startNode["children"].values():
        if child["type"] == NodeType.F:
            size += child["size"]
        else:
            size += calc_dir_size(child)
    return size


def update_size_map(
    path: Tuple[str], item: Tuple[int, NodeType], size_map: SizeMap
) -> SizeMap:
    size, node_type = item
    size_map[path] = (size, node_type)
    path_list = list(path)
    while len(path_list) > 1:
        # print(f"path_list: {path_list} key: {tuple(path_list)}")
        path_list.pop()
        if tuple(path_list) in size_map:
            size_map[tuple(path_list)] = (
                size_map[tuple(path_list)][0] + size,
                size_map[tuple(path_list)][1],
            )

    return size_map


def calc_all_dir_sizes(
    node: FileTree,
    cur_path: List[str],
    size_map: SizeMap,
    parsed_paths: List[List[str]] = [],
) -> SizeMap:
    # print("Size Map 1: \n", size_map)
    startNode = node
    if "root" in node:
        startNode = node["root"]

    for child in startNode["children"].values():
        name = child["name"]
        full_item_path = tuple(cur_path + [name])
        # print(f"cur_path: {cur_path}, full_item_path: {full_item_path}")

        if child["type"] == NodeType.F:
            size_map = update_size_map(
                full_item_path, (child["size"], child["type"]), size_map
            )
            parsed_paths += [full_item_path]

        elif child["type"] == NodeType.D:
            # print(f"Dir: {full_item_path}")
            if not full_item_path in size_map:
                size_map[full_item_path] = (0, NodeType.D)

            if child["children"].values():
                cur_path += [name]
                size_map = calc_all_dir_sizes(child, cur_path, size_map, parsed_paths)

    if len(cur_path) > 1:
        cur_path.pop()

    # print("Size Map 2: \n", size_map)
    return size_map


def process_input(file: str) -> FileTree:
    file_tree = {}
    cur_path = []

    with open(file) as reader:
        commands = reader.read().strip().split("\n")
        for command in commands:
            if command.startswith("$"):
                cmd, *args = command.replace("$ ", "").split(" ")
                if len(args) > 1:
                    raise ValueError(f"Too many args for {cmd}: {args}")

                if cmd == "cd":
                    name = get_node_name(args[0])

                    if name == "..":
                        cur_path.pop()
                    else:
                        cur_path.append(name)

                        if is_root_node(args[0]):
                            if name in file_tree:
                                raise ValueError(f"Duplicate dir: {name}")

                            file_tree[name] = {
                                "name": name,
                                "size": 0,
                                "type": NodeType.D,
                                "children": {},
                            }
                elif cmd != "ls":
                    raise ValueError(f"Unknown command: {cmd}")

            else:
                size, name = command.split(" ")
                name = get_node_name(name)
                target_node = dpath.get(file_tree, "/children/".join(cur_path))[
                    "children"
                ]

                if re.match("\\d+", size):
                    size = int(size)
                    if name in target_node:
                        raise ValueError(f"Duplicate file: {name}")

                    target_node[name] = {
                        "name": name,
                        "size": size,
                        "type": NodeType.F,
                        "children": {},
                    }

                else:
                    if name in target_node:
                        raise ValueError(f"Duplicate dir: {name}")

                    target_node[name] = {
                        "name": name,
                        "size": 0,
                        "type": NodeType.D,
                        "children": {},
                    }

        # print()
        # print("File tree:")
        # pretty_print_tree(file_tree)
        return file_tree


def part_1(node: FileTree) -> int:
    for line in get_tree(copy.deepcopy(node)):
        print(line)

    print()

    sm = {("root",): (0, NodeType.D)}
    calc_all_dir_sizes(node, ["root"], sm, [])
    max_size = 100000
    size = 0
    for s, t in sm.values():
        if t == NodeType.D:
            if s <= max_size:
                size += s
    return size


def part_2(node: FileTree) -> int:
    max_file_size = 70000000
    update_space_needed = 30000000

    sm = {("root",): (0, NodeType.D)}
    calc_all_dir_sizes(node, ["root"], sm, [])
    total_used_space = sm[("root",)][0]
    free_space = max_file_size - total_used_space

    if free_space >= update_space_needed:
        return 0

    # print(f"Total used space: {total_used_space}, free space is {free_space}\n")
    # print(sm)
    # print()
    possible_dir_sizes = []

    for key, (s, t) in sm.items():
        if t == NodeType.D:
            if free_space + s >= update_space_needed:
                possible_dir_sizes.append(s)
    # print(possible_dir_sizes)
    return min(possible_dir_sizes)


def main():
    file_tree = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(file_tree)
    print(f"Part I: {part1_answer} sum of large dirs")
    assert part1_answer == 1206825

    part2_answer = part_2(file_tree)
    print(f"Part II: {part2_answer} is the size of the dir to delete")
    assert part2_answer == 9608311


if __name__ == "__main__":
    main()
