# Day 14

## Data

```python
SAND_START: GridLocation = (500, 0)
START_CHAR = "+"
SAND_CHAR = "o"
ROCK_CHAR = "#"
EMPTY_SPACE_CHAR = "."
InputData = ReservoirMap
```

## Calculations

see ReservoirMap class. Basic graph calc

## Function/Approach

1. create a graph based on falling rocks, set height and width bounds
1. simulate sand until out of bounds, track count
1. return count

## Part II

performance issues

```bash
0.20s user 0.04s system 98% cpu 0.249 total max RSS 22384 # part II test
184.44s user 0.16s system 99% cpu 3:04.72 total max RSS 9772 # part II 5900, did not complete

0.21s user 0.04s system 98% cpu 0.252 total max RSS 21832 # part II memoized
0.38s user 0.02s system 98% cpu 0.404 total max RSS 19364 # part II memoized
```

memoize the last path, start from above the last position
