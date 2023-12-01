# Day 4

## Data

Pair -> Tuple(Tuple(int, int), tuple(int, int))
Pairs of Tuples with lower and upper range

## Calc

are_ranges_inclusive

## Func/approach

1. process input into a list of pairs with ranges
1. for each pair compare ranges, inc count if inclusive

```text
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
```

```python
[
  ((2, 4), (6, 8)),
  ((2, 3), (4, 5)),
  ((5, 7), (7, 9)),
  ((2, 8), (3, 7)),
  ((6, 6), (4, 6)),
  ((2, 6), (4, 8)),
]
```

test cases

(less, less) (more, more)
(less, more) (more, less)
(less, equal) (more, equal)

(equal, equal) (equal, equal)
(equal, less) (equal, more)
(equal, more) (equal, less)

<!-- (less, equal) (more, equal)
(more, equal) (less, equal) -->

(more, more) (less, less)
(more, less) (less, more)
(more, equal) (less, equal)
