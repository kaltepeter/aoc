from functools import lru_cache
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
EXCLUSION_MARKER = "sk"
BEACON_MARKER = "*r"
SENSOR_MARKER = "ob"


class BeaconMap:
    def __init__(self):
        self.sensors: SensorData = SensorData()
        self.beacons: Set[GridLocation] = set()
        self.scanned_data = set()
        self.row_to_check = 0

    def add_beacon(self, location: GridLocation) -> None:
        self.beacons.add(location)

    def add_sensor(self, location: GridLocation, beacon: GridLocation) -> None:
        self.sensors[location] = {
            "nearest_beacon": beacon,
            "distance": distance.cityblock(location, beacon),
        }

    def add_scanned(self, location: GridLocation) -> None:
        if location[1] == self.row_to_check:
            self.scanned_data.add(location)

    def scan_row(
        self,
        scanner_location: GridLocation,
        max_dist: int,
        location: GridLocation,
    ) -> None:
        x, y = location
        while distance.cityblock((x, y), scanner_location) <= max_dist:
            # print(f"scan_row: ({x,y},{location}) <= {max_dist}")
            if (x, y) != scanner_location:
                self.add_scanned((x, y))
                # x mirror
                delta = x - location[0]
                self.add_scanned((scanner_location[0] - delta, y))
            x += 1

    def scan_field(self, location: GridLocation, max_dist: int) -> None:
        x, y = location

        # while distance.cityblock((x, y), location) <= max_dist:
        # print(f"scan_field: ({x,y},{location}) <= {max_dist}")
        self.scan_row(location, max_dist, (x, self.row_to_check))
        # delta = y - location[1]
        # self.scan_row(location, max_dist, (x, location[1] - delta))
        # y += 1


InputData = BeaconMap


def print_plot(data: InputData) -> None:

    border = 1
    beacons = np.array(list(data.beacons))
    sensors = np.array(list(data.sensors))
    scanned = np.array(list(data.scanned_data))
    fig, ax = plt.subplots()
    # ax.set_xlim(data.lowest_x - border, data.highest_x + border)
    # ax.set_ylim(
    #     data.highest_y + border,
    #     data.lowest_y - border,
    # )
    ax.set_aspect("equal", adjustable="datalim")
    ax.tick_params(which="minor", width=1, length=1)
    ax.grid(True, linestyle="-.", markevery=1, snap=True)
    ax.tick_params(labelcolor="b", labelsize="small", width=1)
    tick_spacing = 1
    # plt.xticks(range(data.lowest_x - border, data.highest_x + border + 1, tick_spacing))
    # plt.yticks(range(data.lowest_y - border, data.highest_y + border + 1, tick_spacing))

    plt.rcParams["axes.autolimit_mode"] = "round_numbers"
    if len(scanned) > 0:
        ax.plot(scanned[:, [0]], scanned[:, [1]], EXCLUSION_MARKER, alpha=0.3)

    ax.plot(
        beacons[:, [0]],
        beacons[:, [1]],
        BEACON_MARKER,
    )

    ax.plot(
        sensors[:, [0]],
        sensors[:, [1]],
        SENSOR_MARKER,
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


def part_1(data: InputData, row_check: int) -> int:
    data.row_to_check = row_check
    for sensor, sensor_data in data.sensors.items():
        print(f"sensor: {sensor}, sensor_data: {sensor_data}")
        data.scan_field(sensor, sensor_data["distance"])
    # print_plot(data)
    val = data.scanned_data
    # val = set(filter(lambda val: val[1] == row_check, list(data.scanned_data)))
    val -= data.beacons
    count = len(list(val))

    return count


def part_2(data: InputData) -> int:
    return 0


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi), 2000000)
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 5100463

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
