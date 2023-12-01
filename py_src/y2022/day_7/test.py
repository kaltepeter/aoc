from pathlib import Path
import dpath


my_tree = {
    "root": {
        "a": {
            "value": 2,
            "children": {
                "c": {"value": 4, "children": {}},
            },
        },
        "b": {"value": 3, "children": {}},
    }
}

print(
    dpath.get(
        my_tree,
        "root/a/children/c",
    )
)


# prefix components:
space = "    "
branch = "│   "
# pointers:
tee = "├── "
last = "└── "


# https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
def tree(dir_path: Path, prefix: str = ""):
    """A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters
    """
    contents = list(dir_path.iterdir())
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        yield prefix + pointer + path.name
        if path.is_dir():  # extend the prefix and recurse:
            extension = branch if pointer == tee else space
            # i.e. space because last, └── , above so no more |
            yield from tree(path, prefix=prefix + extension)


for line in tree(Path.home() / "data" / "ka" / "aoc" / "python" / "2022"):
    print(line)
