from copy import deepcopy
import os
from pathlib import Path
from typing import List
from collections import deque


base_path = Path(__file__).parent

Register = List[int]
Program = List[int]
InputData = tuple[Register, Program]


def process_input(file: str) -> InputData:
    register = None
    program = []
    with open(file, "r") as reader:
        register_list, program = reader.read().split("\n\n")
        register = list(map(int, [v.split()[-1] for v in register_list.splitlines()]))
        program = list(map(int, program.replace("Program: ", "").split(',')))

    return (register, program)


def get_combo_operand(registers: Register, op: int) -> int:
    if op in range(4):
        return op
    elif op == 4:
        return registers[0]
    elif op == 5:
        return registers[1]
    elif op == 6:
        return registers[2]
    else:
        raise ValueError(f"Invalid combo operand: {op}")


def dv(registers: Register, op: int) -> int:
    combo = get_combo_operand(registers, op)
    denominator = 2 ** combo
    if denominator == 0:
        return 0
    
    return registers[0] // denominator


def bxl(registers: Register, op: int) -> int:
    return registers[1] ^ op


def bst(registers: Register, op: int) -> int:
    combo = get_combo_operand(registers, op)
    return combo % 8


def bxc(registers: Register, op: int) -> int:
    return registers[1] ^ registers[2]


def out(registers: Register, op: int) -> int:
    combo = get_combo_operand(registers, op)
    return combo % 8


def run_program(register: Register, program: Program) -> tuple[Register, List[int]]:
    instructions = list(zip(program[::2], program[1::2]))
    inst_pointer = 0
    results = []
    while inst_pointer < len(instructions):
        (opcode, operand) = instructions[inst_pointer]
        match opcode:
            case 0:
                register[0] = dv(register, operand)
            case 1:
                register[1] = bxl(register, operand)
            case 2:
                register[1] = bst(register, operand)
            case 3:
                if register[0] != 0:
                    inst_pointer = operand
                    continue
            case 4:
                register[1] = bxc(register, operand)
            case 5:
                results.append(out(register, operand))
            case 6:
                register[1] = dv(register, operand)
            case 7:
                register[2] = dv(register, operand)
        
        inst_pointer += 1

    return (register, results)


def part_1(data: InputData) -> str:
    register, program = data
    results = []
    register, results = run_program(register, program)

    return ",".join(map(str, results))


def find_specific_items(data: InputData, start: int, expected: List[int]) -> int:
    _, program = data
    results = []
    a_bin = start
    while results != expected:
        _, results = run_program([a_bin, 0, 0], program)
        if results == expected:
            break

        a_bin += 1

    print(f"a_value: {a_bin:0b} results: {results}")
    return int(a_bin)


def part_2(data: InputData) -> int:
    _, program = data 
    nums_to_find = deque(program)
    
    a_bin = 0

    while nums_to_find:
        nums_to_find.pop()

        a_value = 0
        results = []
        while results != program:
            test_a_value = (a_bin << 3) | a_value
            _, val = run_program([test_a_value, 0, 0], program)
            results = val
            compare_program = program[::-1]
            if val[::-1] == compare_program[:len(val)]:
                a_bin = test_a_value
                break

            a_value += 1
        else:
            # never hits...
            print('yo')
            a_bin = (a_bin << 3)

    assert results == program
    return a_bin


def main():
    pi = process_input(os.path.join(base_path, "input.txt"))

    part1_answer = part_1(deepcopy(pi))
    print(f"Part I: {part1_answer} \n")
    assert part1_answer == "4,1,7,6,4,1,0,2,7"

    part2_answer = part_2(deepcopy(pi))
    print(f"Part II: {part2_answer} \n")
    assert part2_answer == 164279024971453


if __name__ == "__main__":
    main()
