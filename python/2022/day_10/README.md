# day 10

## data

```python
Func = Literal["noop", "addx"]
Instructions = List[tuple[Func, int]]
interesting_cycles = (20, 60, 100, 140, 180, 220)
```

## calc

signal_strength -> sum([x for x in interesting_cycles])

## func/approach

1. Process instructions
1. iterate on a cycle starting with 1
   1. set register to previous value unless unset, set to 1
   1. pop off first instruction (if length > 0)
      1. if noop, continue
      1. if addx, add to cycles_to_run
      1. if cycles_to_run has something set register
1. return sum of interesting cycles

```text
noop
addx 3
addx -5
```

register = 1

cycles (cmd, val at end):

1. 0, 1
1. +3, 1
1. +3, 4
1. -5, 4
1. -5, -1

```text
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1 # 20
```

register = 1
cycles:

1. +15, 1
1. +15, 16
1. -11, 16
1. -11, 5
1. +6, 5
1. +6, 11
1. -3, 11
1. -3, 8
1. +5, 8
1. +5, 13
1. -1, 13
1. -1, 12
1. -8, 12
1. -8, 4
1. +13, 4
1. +13, 17
1. +4, 17,
1. +4, 21
1. 0, 21
1. -1, 21
1. -1, 20
