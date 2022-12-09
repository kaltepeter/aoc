# Day 8

## Data

```python
TreeRow = List[int]
TreeGrid = List[TreeRow]
VisibleTrees = List[Tuple[int, int]]
```

## Calculations

## func/approach

1. loop through each row in the grid.
   1. loop through each tree
   1. check its row/column for visibility
1. track the visibility and return

```text
30373
25512
65332
33549
35390
```

- if -/+1 in a direction is equal or greater than the tree is not visible, stop processing that direction

Grid x: colPos, y: rowPos
