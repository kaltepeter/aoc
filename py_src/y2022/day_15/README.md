# Day 15

## Data

map of beacons and sensors

```python
Sensor = TypedDict(
    "Sensor", {"position": GridLocation, "closest_beacon": Tuple[int, GridLocation]}
)
Beacons = Set[GridLocation]
Sensors = Set[Sensor]
```

## Calc

## Function/Approach

1. create a map of beacons(known) and sensors
1. store the Manhattan distance and index of the closet beacon for the sensor
1. for each sensor
   1. scan each row to find bounds
   1. after bounds are found, apply the opposite x position
   1. run for opposite y

## Perf

If the top left quadrant is found, apply the top right and bottom half.

```text
..........#
.........##
....S...###
.......####
......#####
.....######
....#######
...########
..#########
.#########S
```

Reverse the manhattan distance?

```python
sum(abs(point1 - point2) for point1, point2 in zip(a, b)) # calc dist
```

Generate all points in range.

Store only edges?

Applying absolutes

```python
from scipy.spatial import distance
distance.cityblock((20,7),(20,1)) # 6
distance.cityblock((20,1),(20,7)) # 6
distance.cityblock((-20,-1),(-20,-7)) # 6
distance.cityblock((-20,1),(-20,7)) # 6
distance.cityblock((20,-1),(20,-7)) # 6
```

1. Cache a lookup.
   1. pair1, pair2 == pair2, pair1 == -pair1, -pair2 == -pair2, -pair1
1. Apply edges

Only store the row of interest

`####B######################`

before:

```bash
pytest py_src/y2022/day_15 1.98s user 0.69s system 205% cpu 1.300 total max RSS 65868
```

after limit:

```bash
pytest py_src/y2022/day_15 1.94s user 0.66s system 222% cpu 1.167 total max RSS 65708
```

## part I slight speed improvement

```bash
python py_src/y2022/day_15/day.py 24.01s user 0.85s system 107% cpu 23.186 total max RSS 1060756
```

```bash
pytest py_src/y2022/day_15 10.61s user 2.29s system 579% cpu 2.228 total max RSS 66272

python py_src/y2022/day_15/day.py 39.92s user 3.83s system 399% cpu 10.951 total max RSS 1949208
```
