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
