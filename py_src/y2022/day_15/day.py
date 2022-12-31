import os
import re
from copy import deepcopy
from pathlib import Path
from typing import Set, TypedDict

import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial import distance

from py_src.shared.graph import GridLocation
from py_src.shared.matplotlib_annotated_cursor import AnnotatedCursor

base_path = Path(__file__).parent

Sensor = TypedDict("Sensor", {"nearest_beacon": GridLocation, "distance": int})
SensorData = dict[GridLocation, Sensor]
ScannedData = Set[GridLocation]

EMPTY_SPACE_CHAR = "."
EXCLUSION_MARKER = "sw"
BEACON_MARKER = "*r"
SENSOR_MARKER = "ob"


class BeaconMap:
    def __init__(self):
        self.lowest_x: int = 0
        self.highest_x: int = 0
        self.lowest_y: int = 0
        self.highest_y: int = 0
        self.sensors: SensorData = SensorData()
        self.beacons: Set[GridLocation] = set()
        self.scanned_data = set()

    def add_beacon(self, location: GridLocation) -> None:
        (x, y) = location
        if x < self.lowest_x:
            self.lowest_x = x
        if x > self.highest_x:
            self.highest_x = x
        if y < self.lowest_y:
            self.lowest_y = y
        if y > self.highest_y:
            self.highest_y = y

        self.beacons.add(location)

    def add_sensor(self, location: GridLocation, beacon: GridLocation) -> None:
        (x, y) = location
        if x < self.lowest_x:
            self.lowest_x = x
        if x > self.highest_x:
            self.highest_x = x
        if y < self.lowest_y:
            self.lowest_y = y
        if y > self.highest_y:
            self.highest_y = y

        self.sensors[location] = {
            "nearest_beacon": beacon,
            "distance": distance.cityblock(location, beacon),
        }

    def scan_field(self, location: GridLocation, max_dist: int) -> set[GridLocation]:
        count = 0
        scanned = set()
        x, y = location
        scanning = True
        while scanning == True:
            if count >= 10:
                scanning = False

            print(f"count: {count}, x: {x}, y: {y}")
            while distance.cityblock((x, y), location) <= max_dist:
                scanned.add((x, y))
                scanned.add((location[0]))
                x += 1
                # print(scanned)

            count += 1
        print()
        return scanned


InputData = BeaconMap


def print_plot(data: InputData) -> None:

    border = 1
    beacons = np.array(list(data.beacons))
    sensors = np.array(list(data.sensors))
    scanned = np.array(list(data.scanned_data))
    print(scanned)
    fig, ax = plt.subplots()
    ax.set_xlim(data.lowest_x - border, data.highest_x + border)
    ax.set_ylim(
        data.highest_y + border,
        data.lowest_y - border,
    )
    ax.set_aspect("equal", adjustable="datalim")
    ax.tick_params(which="minor", width=1, length=1)
    ax.grid(True, linestyle="-.", markevery=1, snap=True)
    ax.tick_params(labelcolor="b", labelsize="small", width=1)
    tick_spacing = 1
    plt.xticks(range(data.lowest_x - border, data.highest_x + border + 1, tick_spacing))
    plt.yticks(range(data.lowest_y - border, data.highest_y + border + 1, tick_spacing))

    plt.rcParams["axes.autolimit_mode"] = "round_numbers"
    ax.fmt_ydata = lambda x: x
    ax.plot(
        beacons[:, [0]],
        beacons[:, [1]],
        BEACON_MARKER,
        label="Beacons",
    )

    ax.plot(
        sensors[:, [0]],
        sensors[:, [1]],
        SENSOR_MARKER,
        label="Sensors",
    )

    if len(scanned) > 0:
        ax.plot(
            scanned[:, [0]],
            scanned[:, [1]],
            EXCLUSION_MARKER,
            label="Sensors",
        )

    plt.show()


# def manhattan_distance(a: GridLocation, b: GridLocation) -> int:
#     return sum(abs(point1 - point2) for point1, point2 in zip(a, b))


def process_input(file: str) -> InputData:
    beacon_map = BeaconMap()
    with open(file, "r") as reader:
        for line in reader.read().split("\n"):
            info = re.findall(
                r"Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)",
                line,
            )
            if len(info) == 0:
                continue
            info = info[0]
            sensor = (int(info[0]), int(info[1]))
            beacon = (int(info[2]), int(info[3]))
            beacon_map.add_sensor(sensor, beacon)
            beacon_map.add_beacon(beacon)
        return beacon_map


def part_1(data: InputData) -> int:
    for sensor, sensor_data in data.sensors.items():
        print(f"sensor: {sensor}, sensor_data: {sensor_data}")
        v = data.scan_field(sensor, sensor_data["distance"])
    print_plot(data)
    # for y in range(data.lowest_y, data.highest_y + 1):
    #     for x in range(data.lowest_x, data.highest_x + 1):
    #         print(f"{x},{y}", end=" ")

    return 0


def part_2(data: InputData) -> int:
    return 0


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 0

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
