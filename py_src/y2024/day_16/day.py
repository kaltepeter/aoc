from collections import deque
from copy import deepcopy
import os
from pathlib import Path
from typing import List
import networkx as nx
from networkx import Graph
from heapq import heappush, heappop


base_path = Path(__file__).parent

Coord = tuple[int, int]
InputData = tuple[Graph, Coord, Coord, int, int]


def process_input(file: str) -> InputData:
    G = nx.DiGraph()  # Use DiGraph instead of Graph
    start = None
    end = None
    max_x = 0
    max_y = 0
    with open(file, "r") as reader:
        for block in reader.read().split("\n\n"):
            lines = block.splitlines()
            max_y = len(lines)
            max_x = len(lines[0])
            for y, row in enumerate(lines):
                for x, char in enumerate(row):
                    if char == "S":
                        start = (x, y)
                    elif char == "E":
                        end = (x, y)

                    if char != "#":
                        G.add_node((x, y))

    for node in G.nodes:
        x, y = node
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            neighbor = (x + dx, y + dy)
            if neighbor in G.nodes:
                G.add_edge(node, neighbor, direction=(dx, dy))

    return (G, start, end, max_x, max_y)


def calc_weight(start: Coord, end: Coord, edge_data: dict) -> int:
    direction = edge_data["direction"]
    x, y = start
    tx, ty = end
    dx, dy = direction
    vector = (tx - x, ty - y)
    if start == end:
        return 0
    
    if vector == direction:
        return 1
    elif vector[0] == -dx and vector[1] == -dy:
        return 2001
    elif vector[0] * dx + vector[1] * dy == 0:
        return 1001
    
    return 0


def print_graph(G: Graph, max_x: int, max_y: int, unique_seen: set[Coord]):
    for y in range(0, max_y):
        for x in range(0, max_x):
            if (x, y) in unique_seen:
                print("O", end="")
            elif (x, y) in G.nodes:
                print(".", end="")
            else:
                print("#", end="")
        print()
    

def find_lowest_cost(data: InputData) -> tuple[int, dict[Coord, Coord]]:
    G, start, end, max_x, max_y = data
    initial_direction = (1, 0)
    
    # Priority queue with (cost, position, direction)
    queue = [(0, start, initial_direction)]
    # Track visited states as (position, direction)
    seen = set()
    costs = {(start, initial_direction): 0}
    path_to = {start: None}
    
    while queue:
        cost, pos, direction = heappop(queue)
        
        if pos == end:
            return (cost, path_to)
            
        if (pos, direction) in seen:
            continue
        
        seen.add((pos, direction))
        
        for neighbor in G.neighbors(pos):
            new_direction = (neighbor[0] - pos[0], neighbor[1] - pos[1])
            new_cost = cost + calc_weight(pos, neighbor, {"direction": direction})
            state = (neighbor, new_direction)
            
            if state not in costs or new_cost < costs[state]:
                costs[state] = new_cost
                path_to[neighbor] = pos
                heappush(queue, (new_cost, neighbor, new_direction))


def part_1(data: InputData) -> int:
    return find_lowest_cost(data)[0]
    

def part_2(data: InputData) -> int:
    G, start, end, max_x, max_y = data
    initial_direction = (1, 0)
    
    # Priority queue with (cost, position, direction)
    queue = [(0, start, initial_direction)]
    costs = {(start, initial_direction): 0}
    backtrack = {}
    best_cost = float("inf")
    end_states = set()
    unique_seen = set()
    
    while queue:
        cost, pos, direction = heappop(queue)
        if cost > costs.get((pos, direction), float("inf")):
            continue

        if pos == end:
            if cost > best_cost:
                break
            best_cost = cost
            end_states.add((pos, direction))
        
        for neighbor in G.neighbors(pos):
            new_direction = (neighbor[0] - pos[0], neighbor[1] - pos[1])
            new_cost = cost + calc_weight(pos, neighbor, {"direction": direction})
            state = (neighbor, new_direction)

            lowest = costs.get(state, float("inf"))
            if new_cost > lowest:
                continue

            if new_cost < lowest:
                backtrack[state] = set()
                costs[state] = new_cost
            
            backtrack[state].add((pos, direction))
            heappush(queue, (new_cost, neighbor, new_direction))
    
    states = deque(end_states)
    seen = set(end_states)

    while states:
        key = states.popleft()
        for last in backtrack.get(key, []):
            if last in seen:
                continue

            seen.add(last)
            states.append(last)


    return len({(x,y) for (x,y), _ in seen})


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 147628

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 670


if __name__ == "__main__":
    main()
