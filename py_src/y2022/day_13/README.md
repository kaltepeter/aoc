# day 13

## data

```python
Packet = List[int | List[int]]
InputData = Tuple[Packet, Packet]
```

## calc

compare_ints -> left <= right
compare_lists -> for each, run compare_ints

## function/approach

1. loop through pairs, keep track of the list of ordered_pairs (index)
   1. recursively pop off the first item in the left and right lists, while lists have items
   1. if the right runs out while the left has length, return false
   1. if the left runs out while the right has length, continue
   1. compare
      1. if one item is an integer and the other is a list convert int to `list[int]`
      1. if both are int, run compare_int
1. return sum of the index of ordered pairs

`[1,[2,[3,[4,[5,6,7]]]],8,9] vs [1,[2,[3,[4,[5,6,0]]]],8,9]`
