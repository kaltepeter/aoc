from copy import deepcopy
from heapq import heappop, heappush
import os
from pathlib import Path
from typing import List
from networkx import Graph
import networkx as nx
from collections import Counter

base_path = Path(__file__).parent

Coord = tuple[int, int]
CheatCoords = tuple[Coord, Coord]
InputData = tuple[Coord, Coord, Graph, set[Coord], int, int]

neighbor_coords = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def manhattan_distance(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def process_input(file: str) -> InputData:
    G = Graph()
    start = None
    end = None
    walls = set()
    valid_positions = {}
    
    with open(file, "r") as reader:
        map = reader.read().split("\n\n")[0]
        lines = map.splitlines()
        max_y, max_x = len(lines), len(lines[0])
        
        # Process all positions in one pass
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                pos = (x, y)
                
                if c == "#":
                    if 0 < x < max_x - 1 and 0 < y < max_y - 1:
                        walls.add(pos)
                else:
                    # Store valid neighbors during initial scan
                    neighbors = []
                    for dx, dy in neighbor_coords:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < max_x and 0 <= ny < max_y:
                            neighbors.append((nx, ny))
                    valid_positions[pos] = neighbors
                    G.add_node(pos)
                    
                    if c == "S":
                        start = pos
                    elif c == "E":
                        end = pos

    # Add edges in one batch operation
    for pos, neighbors in valid_positions.items():
        for neighbor in neighbors:
            if neighbor in valid_positions:
                G.add_edge(pos, neighbor)

    return (start, end, G, walls, max_x, max_y)


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
        if neighbor in graph.nodes:
            neighbors.append(neighbor)

    return neighbors


def get_cheated_grid(graph: Graph, walls: set[Coord], cheat: CheatCoords) -> tuple[Graph, set[Coord]]:
    cheated_graph = deepcopy(graph)
    cheated_walls = deepcopy(walls)
    cheat1, cheat2 = cheat

    if cheat1 in cheated_walls:
        cheated_graph.add_node(cheat1)
        cheated_walls.remove(cheat1)
        for neighbor in get_neighbors(cheat1, cheated_graph):
            cheated_graph.add_edge(cheat1, neighbor)
            cheated_graph.add_edge(neighbor, cheat1)

    if cheat2 in cheated_walls:
        cheated_walls.remove(cheat2)
        cheated_graph.add_node(cheat2)
        for neighbor in get_neighbors(cheat2, cheated_graph):
            cheated_graph.add_edge(cheat2, neighbor)
            cheated_graph.add_edge(neighbor, cheat2)

    return (cheated_graph, cheated_walls)


def a_star(start: Coord, end: Coord, graph: Graph, walls: set[Coord]) -> int:
    frontier = [(0, start)]  # priority queue of (f_score, position)
    came_from = {start: None}
    g_score = {start: 0}     # cost from start to current node
    
    while frontier:
        _, current = heappop(frontier)
        
        if current == end:
            return g_score[current]
            
        for next_pos in get_neighbors(current, graph):
            tentative_g = g_score[current] + 1
            
            if next_pos not in g_score or tentative_g < g_score[next_pos]:
                came_from[next_pos] = current
                g_score[next_pos] = tentative_g
                f_score = tentative_g + manhattan_distance(next_pos, end)
                heappush(frontier, (f_score, next_pos))
    
    return float('inf')  # No path found


def get_cheats_saving_x_seconds(counts: dict[int, int], seconds_to_save: int) -> int:
    return sum([count for time, count in counts.items() if time >= seconds_to_save])


def part_1(data: InputData) -> dict[int, int]:
    start, end, graph, walls, max_x, max_y = data

    path_time = a_star(start, end, graph, walls)
    print(f"path_time: {path_time}")
    cheated_times = []

    cheats = find_cheats(graph, walls)
    for cheat in cheats:
        cheated_grid, cheated_walls = get_cheated_grid(graph, walls, cheat)
        cheated_path_time = a_star(start, end, cheated_grid, cheated_walls)
        if cheated_path_time < path_time:
            cheated_times.append(cheated_path_time)
        # print_grid(cheated_grid, max_x, max_y, cheated_walls, path=None, cheat=cheat)
        # print(f"cheated_path_time: {cheated_path_time} for cheat {cheat}")

    time_savings = [path_time - cheated_time for cheated_time in cheated_times]

    return Counter(time_savings)


def part_2(data: InputData) -> int:
    return 0


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    counts_part_1 = part_1(deepcopy(pi))
    part1_answer = get_cheats_saving_x_seconds(counts_part_1, 100)
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 0

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 0


if __name__ == "__main__":
    main()
