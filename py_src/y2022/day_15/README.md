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
1.
