# Day 9

## Data

```python
Dir = Literal["U", "D", "L", "R"]
Move = Tuple[Dir, int]
Moves = List[Move]
```

## Calculations

is_touching -> (h, t) greater than 1 in either dir

## Func/Process

1. Loop through the list of commands
   1. loop through each step
   1. execute head move
   1. execute tail move (h - 1)
   1. if not touching move 1 in previous dir
1. track positions and return count

```text
move: ('R', 4)
head: (4, 0) tail: (3, 0)
move: ('U', 4)
head: (4, -4) tail: (3, -3)
move: ('L', 3)
head: (1, -4) tail: (1, -3)
move: ('D', 1)
head: (1, -3) tail: (1, -3)
move: ('R', 4)
head: (5, -3) tail: (4, -3)
move: ('D', 1)
head: (5, -2) tail: (4, -3)
move: ('L', 5)
head: (0, -2) tail: (0, -3)
move: ('R', 2)
head: (2, -2) tail: (1, -3)
```
