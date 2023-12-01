from functools import lru_cache
from itertools import chain
import os
import re
from copy import deepcopy
from pathlib import Path
from typing import List, Set, TypedDict
import multiprocessing

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
    ) -> Set[GridLocation]:
        x, y = location
        results = set()
        while distance.cityblock((x, y), scanner_location) <= max_dist:
            # print(f"scan_row: ({x,y},{location}) <= {max_dist}")
            if (x, y) != scanner_location:
                results.add((x, y))
                # self.add_scanned((x, y))
                # x mirror
                delta = x - location[0]
                results.add((scanner_location[0] - delta, y))
                # self.add_scanned((scanner_location[0] - delta, y))
            x += 1
        return results

    def scan_field(self, sensor_data: SensorData) -> Set[GridLocation]:
        location = sensor_data[0]
        x, y = location
        max_dist = sensor_data[1]["distance"]
        # print(f"sensor: {location}, sensor_data: {sensor_data}")

        # while distance.cityblock((x, y), location) <= max_dist:
        # print(f"scan_field: ({x,y},{location}) <= {max_dist}")
        return self.scan_row(location, max_dist, (x, self.row_to_check))
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


def is_free(point: tuple[int, int], sensors: SensorData) -> bool:
    """Returns True if point is outside the exclusion range of every sensor in sensors"""
    for sensor, sensor_data in sensors.items():
        (x, y) = point
        if distance.cityblock((x, y), sensor) <= sensor_data["distance"]:
            return False
    return True


def part_1(data: InputData, row_check: int) -> int:
    data.row_to_check = row_check
    results: List[Set[GridLocation]] = list()
    with multiprocessing.Pool() as pool:
        results = pool.map(data.scan_field, data.sensors.items())
    exclusion_zone = set(chain.from_iterable(results))
    # for sensor, sensor_data in data.sensors.items():
    #     print(f"sensor: {sensor}, sensor_data: {sensor_data}")
    #     data.scan_field(sensor, sensor_data["distance"])
    # print_plot(data)
    # val = data.scanned_data
    val = exclusion_zone
    # val = set(filter(lambda val: val[1] == row_check, list(data.scanned_data)))
    val -= data.beacons
    count = len(list(val))

    return count


def part_2(data: InputData, max_range: int) -> int:
    # https://byjus.com/maths/slope-intercept-form/
    # https://github.com/BuonHobo/advent-of-code/blob/master/2022/15/Alex/second.py
    lines: dict[tuple[bool, int], int] = {}
    for sensor, sensor_data in data.sensors.items():
        top_rising = (
            True,  # m is 1
            sensor[1] - sensor_data["distance"] - 1 - sensor[0],  # this is q
        )

        top_descending = (
            False,  # m is -1
            sensor[1] - sensor_data["distance"] - 1 + sensor[0],
        )

        bottom_rising = (
            True,
            sensor[1] + sensor_data["distance"] + 1 - sensor[0],
        )

        bottom_descending = (
            False,
            sensor[1] + sensor_data["distance"] + 1 + sensor[0],
        )

        for line in [top_rising, top_descending, bottom_rising, bottom_descending]:
            """I'm counting the occurrences of each line"""
            if line in lines:
                lines[line] += 1
            else:
                lines[line] = 1

    rising_lines: list[int] = []
    descending_lines: list[int] = []

    for line, count in lines.items():
        """
        I only keep the lines that appear at least two times.
        I do this because I know that the single free spot lies where 4 lines intersect
        (2 rising and 2 descending)
        """
        if count > 1:
            if line[0]:
                descending_lines.append(line[1])
            else:
                rising_lines.append(line[1])

    points: list[tuple[int, int]] = []

    for rising_q in rising_lines:
        for descending_q in descending_lines:
            """I calculate the intersections between all the rising and descending lines i got"""
            x = (rising_q - descending_q) // 2
            y = x + descending_q
            point = (x, y)
            points.append(point)

    for point in points:
        """I check which of the intersections is the free point"""
        if (
            (0 <= point[1] <= max_range)
            and (0 <= point[0] <= max_range)
            and is_free(point, data.sensors)
        ):
            return point[0] * 4000000 + point[1]

    raise ValueError  # If the point is not found then the input is wrong


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi), 2000000)
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 5100463

    part2_answer = part_2(deepcopy(pi), 4000000)
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 11557863040754


if __name__ == "__main__":
    main()
