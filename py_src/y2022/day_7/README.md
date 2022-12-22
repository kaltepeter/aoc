# Day 6

## Data

Node = Dict{name: str, type: FILE|DIR, size: int, children: List[Node]}
FileTree = List[Node]

## Calc

calc_dir_size -> parent node, sum all children

## Func/Approach

1. Process input into a list of strings
1. Loop through each command
   1. `cd` create a node, store partial path
   1. `ls` read each line and attach as child nodes
1. step through each node and calc dir sizes, filter by most 100000

## Data Issues

```text
└── root (dir, size=0)
    ├── bntdgzs (dir, size=0)
    │   └── gcwcp (file, size=297955)
    ├── cjw.jgc (file, size=179593)
    ├── grbwdwsm.znn (file, size=110209)
    ├── hsswswtq (dir, size=289802)
    │   ├── bsjbvff (dir, size=289802)
    │   │   ├── dmnt (dir, size=289802)
    │   │   │   └── zht (file, size=221038)
    │   │   ├── grbwdwsm.znn (file, size=148799)
    │   │   ├── grbwdwsm.znn (file, size=148799)
```

The last two lines are likely the same file reference, if the name and size match don't recreate

In the data `148799 grbwdwsm.znn` only exists once, throw an error in this scenario

## Trees

```text
└── root (dir, size=736556)
    ├── bntdgzs (dir, size=446754)
    |   ├── grbwdwsm.znn (file, size=148799)
    │   └── gcwcp (file, size=297955)
    ├── cjw.jgc (file, size=179593)
    └── grbwdwsm.znn (file, size=110209)
```

```python
{
  "root": {
    "name": 'root', "size": 0, "type": "DIR", "children": {
      "bntdgzs": {
        "name": 'bntdgzs', "size": 0, "type": "DIR", "children": {
          "grbwdwsm.znn": {
            "name": 'grbwdwsm.znn', "size": 148799, "type": "FILE", "children":{}
          },
          "gcwcp": {
            "name": 'gcwcp', "size": 297955, "type": "FILE", "children":{}
          }
        }
      }
      "cjw.jgc": {
        "name": 'cjw.jgc', "size": 179593, "type": "FILE", "children": {}
      }
      "grbwdwsm.znn": {
        "name": 'grbwdwsm.znn', "size": 110209, "type": "FILE", "children": {}
      }
    }
  }
}
```

```python
{
  ('root', 'bntdgzs', 'grbwdwsm.znn'): 148799,
  ('root', 'bntdgzs', 'gcwcp'): 297955,
  ('root', 'bntdgzs'): 446754,
  ('root', 'cjw.jgc'): 179593,
  ('root', 'grbwdwsm.znn'): 110209,
  ('root'): 736556
}
```

1. depth-first traversal
1. store path along the way
1. once a file is hit, pop off the tuple updating counts for each level

Calc:

1. loop through size dict
1. filter on values <= max_size
1. sum together

### Alternate structure

```python
[
    {"id": 1, "name": 'root', "size": 0, "type": "DIR", "children": [2], "path": ()},
    {"id": 2, "name": 'bntdgzs', "size": 0, "type": "DIR", "children": [3,6], "path": ('root')},
    {"id": 6, "name": 'grbwdwsm.znn', "size": 148799, "type": "FILE", "children": [], "path": ('root', 'bntdgzs')}
    {"id": 3, "name": 'gcwcp', "size": 297955, "type": "FILE", "children": [], "path": ('root', 'bntdgzs')},
    {"id": 4, "name": 'cjw.jgc', "size": 179593, "type": "FILE", "children": [], "path": ('root')},
    {"id": 5, "name": 'grbwdwsm.znn', "size": 110209, "type": "FILE", "children": [], "path": ('root')},
]
```

This would be much easier to get the size_map
