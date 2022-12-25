# day 12

## data

height_map_graph -> weighted graph of nodes and edges
position -> Coord
best_signal_position -> Coord

```python
Coord = Tuple[int, int]
MAX_HEIGHT_DIFF = 1
```

## calc

get_value -> ord('a')
is_higher -> ord('a') < ord('c')
is_in_range -> math.abs(ord('a') - ord('b')) <= MAX_HEIGHT_DIFF

## function/approach

1.

```python
print([a for a in range(ord('a'), ord('z')+1)])
# [97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122]
print([chr(a) for a in range(ord('a'), ord('z')+1)])
# ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
```

0.22s user 0.06s system 97% cpu 0.277 total max RSS 22472

```text
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
```

```text
@..@@@@@
@@.@@@@@
.@@@@E@@
..@@@@@@
..@@@@@@
```

```text
m=109
n=110
o=111

111 - 109 = 3
106 - 109 = -3
z=122
E=123
```
