from copy import deepcopy
from itertools import combinations
import os
from pathlib import Path
from typing import List
from graphviz import Digraph

dot = Digraph()

base_path = Path(__file__).parent

FormulaList = tuple[str, str, str]
RuleMap = dict[tuple[str, str], List[tuple[str, str]]]
WireMap = dict[str, int]
InputData = tuple[WireMap, RuleMap]


operators = {
    "AND": lambda x, y: x & y,
    "OR": lambda x, y: x | y,
    "XOR": lambda x, y: x ^ y,
}


def process_input(file: str) -> InputData:
    wire_map = {}
    rule_map = {}
    with open(file, "r") as reader:
        val_list, rule_list = reader.read().split("\n\n")
        for val in val_list.splitlines():
            wire, value = val.split(": ")
            wire_map[wire] = int(value)

        for rule in rule_list.splitlines():
            inputs, output = rule.split(" -> ")
            input1, op, input2 = inputs.split(" ")
            if (input1, input2) not in rule_map:
                rule_map[(input1, input2)] = []

            rule_map[(input1, input2)].append((op, output))

    return (wire_map, rule_map)


def calculate_letter_values(wire_map: WireMap, letter: str) -> int:
    z_values = sorted([key for key in wire_map.keys() if key.startswith(letter)], reverse=True)
    bits = "".join([str(wire_map[val]) for val in z_values])
    if len(bits) < 1:
        return 0
    
    return int(bits, 2)


def simulate_gates(wire_map: WireMap, rule_map: RuleMap, z_list: set[str]) -> tuple[WireMap, set[str]]:
    for inputs, outputs in rule_map.items():
        for output in outputs:
            (op, output) = output
            if output not in z_list and output.startswith("z"):
                # gate already found
                continue 

            if all([input in wire_map for input in inputs]):
                input1, input2 = inputs
                wire_map[output] = operators[op](wire_map[input1], wire_map[input2])
                if output.startswith("z"):
                    z_list.remove(output)

    return (wire_map, z_list)


def is_list_valid(wire_map: WireMap) -> bool:
    xs = calculate_letter_values(wire_map, 'x')
    ys = calculate_letter_values(wire_map, 'y')
    zs = calculate_letter_values(wire_map, 'z')

    return xs + ys == zs
    

def get_swaps(wire_map: WireMap) -> List[tuple[str, str]]:
    pairs = combinations(wire_map.keys(), 2)
    swaps = []

    for pair in pairs:
        is_valid = is_list_valid(wire_map)
        if is_valid:
            return swaps  
        
        pair0_suffix = pair[0][1:]
        pair1_suffix = pair[1][1:]
        zs = [f"z{pair0_suffix}", f"z{pair1_suffix}"]
        if len(zs) == 0:
            raise ValueError("No zs found")
        
        swap = {
            pair[0]: wire_map[pair[0]],
            pair[1]: wire_map[pair[1]],
            zs[0]: wire_map[zs[0]],
            zs[1]: wire_map[zs[1]],
        }
        is_valid = is_list_valid(swap)
        if is_valid:
            continue

        print(f"{pair}: {wire_map[pair[0]]} {wire_map[pair[1]]} is_valid: {is_valid}, zs: {zs}")
        print(swap)
        swap[pair[0]] = swap[pair[1]]
        swap[pair[1]] = swap[pair[0]]
        is_valid = is_list_valid(swap)
        if is_valid:
            continue
        else:
            swaps.append(pair)

    print(is_list_valid(wire_map))

    return []


def process_wires(wire_map: WireMap, rule_map: RuleMap) -> WireMap:
    z_list = {z for rules in rule_map.values() for _, z in rules if z.startswith("z")}

    while z_list:
        wire_map, z_list = simulate_gates(wire_map, rule_map, z_list)

    return wire_map


def sort_key(item):
    (input1, input2) = item[0]
    # Get numeric parts of inputs
    digit1 = int(input1[1:]) if input1[1:].isdigit() else 0
    digit2 = int(input2[1:]) if input2[1:].isdigit() else 0

    # Priority order: x/y first, then numeric order
    prefix_priority = {'x': 0, 'y': 1}.get(input1[0], 2)

    return (prefix_priority, digit1, digit2)


def print_diagram(rule_map: RuleMap) -> None: 
    rule_map_items = sorted(rule_map.items(), key=sort_key)
    with open(os.path.join(base_path, "diagram.md"), "w") as writer:
        writer.write("```mermaid\n")
        writer.write("---\n")
        writer.write("wire map\n")
        writer.write("---\n")
        writer.write("flowchart TD\n")
        for (input1, input2), outputs in rule_map_items:
            digit1 = int(input1[1:]) if input1[1:].isdigit() else 0
            digit2 = int(input2[1:]) if input2[1:].isdigit() else 0
            print(f"{input1} {input2} {digit1} {digit2}")
            if digit1 > digit2:
                input1, input2 = input2, input1

            for output in outputs:
                (op, output) = output
                style = "AND" if op == "AND" else "OR" if op == "OR" else "XOR"
                writer.write(f"{input1} --> op_{input1}_{input2}[{op}]\n")
                writer.write(f"{input2} --> op_{input1}_{input2}\n")
                writer.write(f"op_{input1}_{input2}:::{op} --> {output}\n")
        writer.write(f"classDef AND stroke:#f00\n")
        writer.write("classDef OR stroke:#0f0\n")
        writer.write("classDef XOR stroke:#00f\n")
        writer.write("```\n")


def print_wire_tree(formulas: FormulaList, wire: str, depth: int = 0) -> None:
    if wire[0] in "xy":
        return "  " * depth + wire
    op, x, y = formulas[wire]
    return "  " * depth + op + " (" + wire + ")\n" + print_wire_tree(formulas, x, depth + 1) + "\n" + print_wire_tree(formulas, y, depth + 1)


def make_wire(prefix: str, num: int) -> str:
    return f"{prefix}{num:02d}"


def verify_intermediate_xor(formulas: FormulaList, wire: str, num: int) -> bool:
    if wire not in formulas:
        return False
    # print(f"vx", wire, num)
    op, x, y = formulas[wire]
    if op != 'XOR':
        return False
    return sorted([x, y]) == [make_wire('x', num), make_wire('y', num)]


def verify_direct_carry(formulas: FormulaList, wire: str, num: int) -> bool:
    if wire not in formulas:
        return False
    # print(f"vd", wire, num)
    op, x, y = formulas[wire]
    if op != 'AND':
        return False
    return sorted([x, y]) == [make_wire('x', num), make_wire('y', num)]


def verify_recarry(formulas: FormulaList, wire: str, num: int) -> bool:
    if wire not in formulas:
        return False
    # print(f"vr", wire, num)
    op, x, y = formulas[wire]
    if op != 'AND':
        return False
    return verify_intermediate_xor(formulas, x, num) and verify_carry_bit(formulas, y, num) or verify_intermediate_xor(formulas, y, num) and verify_carry_bit(formulas, x, num)
    

def verify_carry_bit(formulas: FormulaList, wire: str, num: int) -> bool:
    if wire not in formulas:
        return False
    # print('vc', wire, num)
    op, x, y = formulas[wire]
    if num == 1:
        if op != 'AND':
            return False
        return sorted([x, y]) == ['x00', 'y00']
    if op != 'OR':
        return False
    return verify_direct_carry(formulas, x, num - 1) and verify_recarry(formulas, y, num - 1) or verify_direct_carry(formulas, y, num - 1) and verify_recarry(formulas, x, num - 1)


def verify_z(formulas: FormulaList, wire: str, num: int) -> bool:
    if wire not in formulas:
        return False
    # print('vz', wire, num)
    op, x, y = formulas[wire]
    if op != 'XOR':
        return False
    if num == 0:
        return sorted([x, y]) == ['x00', 'y00']
    return verify_intermediate_xor(formulas, x, num) and verify_carry_bit(formulas, y, num) or verify_intermediate_xor(formulas, y, num) and verify_carry_bit(formulas, x, num)


def verify(formulas: FormulaList, num: int) -> bool:
    return verify_z(formulas, make_wire('z', num), num)


def draw_graph(wire_map: WireMap, rule_map: RuleMap) -> None:
    for wire, value in wire_map.items():
        dot.node(wire, f"{wire}\n{value}")

        for (input1, input2), outputs in rule_map.items():
            for (op, output) in outputs:

                color = "black"
                if op == "AND":
                    color = "red"
                elif op == "OR":
                    color = "blue"
                elif op == "XOR":
                    color = "green"

                dot.edge(input1, output, label=op, color=color)
                dot.edge(input2, output, label=op, color=color)

        dot.render("circuit_graph", format="png", view=True) 


def progress(formulas: FormulaList) -> int:
    i = 0 
    while True:
        if not verify(formulas, i):
            break
        i += 1

    return i


def part_1(data: InputData) -> int:
    wire_map, rule_map = data
    
    wire_map = process_wires(wire_map, rule_map)

    return calculate_letter_values(wire_map, 'z')


def part_2(data: InputData) -> str:
    _, rule_map = data
    # draw_graph(wire_map, rule_map)

    formulas = {}
    swaps = []

    for (input1, input2), outputs in rule_map.items():
        for (op, output) in outputs:
            formulas[output] = (op, input1, input2)

    for _ in range(4):
        baseline = progress(formulas)
        for x in formulas:
            for y in formulas:
                if x == y: 
                    continue
                formulas[x], formulas[y] = formulas[y], formulas[x]
                if progress(formulas) > baseline:
                    break
                formulas[x], formulas[y] = formulas[y], formulas[x]
            else:
                continue
            break
        swaps += [x, y]
        # print(f"found {x, y}")
    
    # i = progress(formulas)
        
    # wire = make_wire('z', i)
    # print(f"failed on {wire}")
    # print(print_wire_tree(formulas, wire, i))

    # frn <--> z05
    # wnf <--> vtj
    #  

    return ",".join(sorted(swaps))


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == 56939028423824

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == "frn,gmq,vtj,wnf,wtt,z05,z21,z39"


if __name__ == "__main__":
    main()
