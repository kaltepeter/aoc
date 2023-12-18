# Day 14

## Approach

1. loop through the rows (range 1, len(data))
1. if prev_row value is ., move char up
1. calculate totals

```text
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
```

reversed:

```text
#....###..
#OO..#....

#OO..###..
#....#....
```
