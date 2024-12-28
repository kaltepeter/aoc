from copy import deepcopy
from heapq import heappop, heappush
import os
from pathlib import Path
from typing import List
from tqdm import tqdm

base_path = Path(__file__).parent

Coord = tuple[int, int]
CheatCoords = tuple[Coord, Coord]
Graph = List[List[str]]
InputData = tuple[Graph, Coord, Coord]

neighbor_coords = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def manhattan_distance(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def process_input(file: str) -> InputData:    
    graph = []
    with open(file, "r") as reader:
        block = reader.read().split("\n\n")
        graph = [list(line.strip()) for line in block[0].splitlines()]

    for y, line in enumerate(graph):
        for x, char in enumerate(line):
            if char == "S":
                start = (x, y)
            if char == "E":
                end = (x, y)
      
    return (graph, start, end)


def find_cheats(graph: Graph, walls: set[Coord]) -> set[CheatCoords]:
    cheats = set()
    for x, y in walls:
        for dx, dy in neighbor_coords:
            neighbor = (x + dx, y + dy)
            if neighbor in graph.nodes:
                cheats.add(((x, y), neighbor))
                break
             
    return cheats
 

def print_grid(grid: Graph, max_x: int, max_y: int, walls: List[Coord] = None, path: List[Coord] = None, cheat: CheatCoords = None):
    walls = walls or []
    path = path or []
    cheat1, cheat2 = cheat or (None, None)
    for y in range(max_y):
        for x in range(max_x):
            if (x, y) == cheat1 or (x, y) == cheat2:
                print("1", end="")
            else:
                if (x, y) in walls or x == 0 or y == 0 or x == max_x - 1 or y == max_y - 1:
                    print("#", end="")
                elif (x, y) in path:
                    print("O", end="")
                else:
                    print(".", end="")



        print()


def get_neighbors(coord: Coord, graph: Graph) -> list[Coord]:
    neighbors = []
    x, y = coord
    for dx, dy in neighbor_coords:
        neighbor = (x + dx, y + dy)
        if graph[neighbor[1]][neighbor[0]] != "#":
            neighbors.append(neighbor)

    return neighbors


# def get_cheated_grid(graph: Graph, walls: set[Coord], cheat: CheatCoords) -> tuple[Graph, set[Coord]]:
#     cheated_graph = deepcopy(graph)
#     cheated_walls = deepcopy(walls)
#     cheat1, cheat2 = cheat

#     if cheat1 in cheated_walls:
#         cheated_graph.add_node(cheat1)
#         cheated_walls.remove(cheat1)
#         for neighbor in get_neighbors(cheat1, cheated_graph):
#             cheated_graph.add_edge(cheat1, neighbor)
#             cheated_graph.add_edge(neighbor, cheat1)

#     if cheat2 in cheated_walls:
#         cheated_walls.remove(cheat2)
#         cheated_graph.add_node(cheat2)
#         for neighbor in get_neighbors(cheat2, cheated_graph):
#             cheated_graph.add_edge(cheat2, neighbor)
#             cheated_graph.add_edge(neighbor, cheat2)

#     return (cheated_graph, cheated_walls)


def a_star(start: Coord, end: Coord, graph: Graph) -> List[Coord]:
    frontier = [(0, start)]  # priority queue of (f_score, position)
    came_from = {start: None}
    g_score = {start: 0}     # cost from start to current node
    
    while frontier:
        _, current = heappop(frontier)
        
        if current == end:
            # Reconstruct path
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1]
            
        for next_pos in get_neighbors(current, graph):
            tentative_g = g_score[current] + 1
            
            if next_pos not in g_score or tentative_g < g_score[next_pos]:
                came_from[next_pos] = current
                g_score[next_pos] = tentative_g
                f_score = tentative_g + manhattan_distance(next_pos, end)
                heappush(frontier, (f_score, next_pos))
    
    return []  # No path found


# def get_cheats_saving_x_seconds(counts: dict[int, int], seconds_to_save: int) -> int:
#     return sum([count for time, count in counts.items() if time >= seconds_to_save])


def is_in_grid(coord: Coord, max_x: int, max_y: int) -> bool:
    return 0 <= coord[0] < max_x and 0 <= coord[1] < max_y


def part_1(data: InputData, max_dist: int = 100) -> int:
    graph, start, end = data
    rows, cols = len(graph), len(graph[0])

    path = a_star(start, end, graph)
    path_time = len(path) - 1

    dists = {}
    for t, coord in enumerate(path):    
        dists[coord] = path_time - t

    saved = {}
    for t, coord in enumerate(tqdm(path, ncols=80)):
        x, y = coord
        for dx1, dy1 in neighbor_coords:
            for dx2, dy2 in neighbor_coords:
                xx, yy = x + dx1 + dx2, y + dy1 + dy2
                if not is_in_grid((xx, yy), cols, rows) or graph[yy][xx] == "#":
                    continue

                remaining_time = dists[(xx, yy)]
                saved[(x, y, xx, yy)] = path_time - (t + remaining_time + 2)


    count = 0       
    for v in saved.values():
        if v >= max_dist:
            count += 1

    return count


def part_2(data: InputData, max_dist: int = 100) -> int:
    graph, start, end = data
    rows, cols = len(graph), len(graph[0])

    path = a_star(start, end, graph)
    path_time = len(path) - 1
    max_cheat = 20

    dists = {}
    for t, coord in enumerate(path):    
        dists[coord] = path_time - t

    saved = {}
    for t, coord in enumerate(tqdm(path, ncols=80)):
        x, y = coord
        for xx in range(x - max_cheat, x + max_cheat + 1):
            for yy in range(y - max_cheat, y + max_cheat + 1):
                time_used = abs(xx - x) + abs(yy - y)
                if not is_in_grid((xx, yy), cols, rows) or time_used > max_cheat or graph[yy][xx] == "#":
                    continue

                remaining_time = dists[(xx, yy)]
                saved[(x, y, xx, yy)] = path_time - (t + remaining_time + time_used)

    count = 0
    for v in saved.values():
        if v >= max_dist:
            count += 1
    
    return count


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 1511

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 1020507


if __name__ == "__main__":
    main()

