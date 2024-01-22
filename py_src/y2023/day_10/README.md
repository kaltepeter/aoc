# Day 10

- `|` is a vertical pipe connecting north and south.
- `-` is a horizontal pipe connecting east and west.
- `L` is a 90-degree bend connecting north and east.
- `J` is a 90-degree bend connecting north and west.
- `7` is a 90-degree bend connecting south and west.
- `F` is a 90-degree bend connecting south and east.
- `.` is ground; there is no pipe in this tile.
- `S` is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

`InputData: List[str]`

Lookup pattern:

`x` column index
`y` row index

`current`: `[y][x]`
`east` : `[y][x+1]`
`west` : `[y][x-1]`
`north` : `[y-1][x]`
`south` : `[y+1][x]`

`|`: connects `line[y+1][x]` and `line[y-1][x]`
`-`: connects `line[y][x+1]` and `line[y][x-1]`
`L`: connects `line[y-1][x]` and `line[y][x+1]`
`J`: connects `line[y-1][x]` and `line[y][x-1]`
`7`: connects `line[y+1][x]` and `line[y][x-1]`
`F`: connects `line[y+1][x]` and `line[y][x+1]`
`.`: nothing
`S`: start

```python
class CharMap(Enum):
    EMPTY = "."
    START = "S"
    PIPE = "|"
    DASH = "-"
    EL = "L"
    JAY = "J"
    SEVEN = "7"
    EFF = "F"

pipe_map = {
  (0, 1): [CharMap.PIPE, CharMap.SEVEN, CharMap.EFF],
  (0, -1): [CharMap.PIPE, CharMap.EL, CharMap.JAY],
  (1, 0): [CharMap.DASH, CharMap.EL, CharMap.EFF],
  (-1, 0): [CharMap.DASH, CharMap.JAY, CharMap.SEVEN]
}

# lookup via +/- x or y
# i.e. (0,1) = y+1, x
```

## approach

1. figure out what the start is (max 2 pipes)
1. optionally filter out not connected
1. follow both paths, counting the steps
1. return max of both paths

(1,1),

(1,1),(2,1)
pipes = (1,1) or (3,1)
(1,1),(2,1)

if key in
