import os
import sys
import re
import copy
import time

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test_part2.txt")
inputfile = os.path.join(dirname, "input.txt")


class LoopError(Exception):
    pass


class Memory:
    def __init__(self, a, b, c):
        self.register_a = a
        self.original_a = a
        self.original_bits = 10
        self.bits = self.original_bits
        self.register_b = b
        self.register_c = c
        self.instruction_pointer = 0
        self.output = []

    def jump(self, operand):
        self.instruction_pointer = operand

    def shift_a(self, i):
        self.register_a = int(
            f"{i:>03b}{self.register_a:>0{self.original_bits - 3}b}", 2
        )
        self.original_a = int(f"{i:>03b}{self.original_a:>0{self.bits}b}", 2)
        self.bits += 3

    def combo_operand(self, operand):
        if operand in [0, 1, 2, 3]:
            return operand
        if operand == 4:
            return self.register_a
        if operand == 5:
            return self.register_b
        if operand == 6:
            return self.register_c

    def increment_instruction_pointer(self):
        self.instruction_pointer += 2


class Instruction:
    OPCODE = None

    def execute(self, operand, memory):
        pass


class Adv(Instruction):
    OPCODE = 0

    def execute(self, operand, memory):
        operand = memory.combo_operand(operand)
        memory.register_a = memory.register_a >> operand
        memory.increment_instruction_pointer()


class Bxl(Instruction):
    OPCODE = 1

    def execute(self, operand, memory):
        memory.register_b = memory.register_b ^ operand
        memory.increment_instruction_pointer()


class Bst(Instruction):
    OPCODE = 2

    def execute(self, operand, memory):
        memory.register_b = memory.combo_operand(operand) & 7
        memory.increment_instruction_pointer()


class Jnz(Instruction):
    OPCODE = 3

    def execute(self, operand, memory):
        if memory.register_a != 0:
            memory.jump(operand)
        else:
            memory.increment_instruction_pointer()


class Bxc(Instruction):
    OPCODE = 4

    def execute(self, operand, memory):
        memory.register_b = memory.register_b ^ memory.register_c
        memory.increment_instruction_pointer()


class Out(Instruction):
    OPCODE = 5

    def execute(self, operand, memory):
        memory.output.append(memory.combo_operand(operand) & 7)
        memory.increment_instruction_pointer()


class Bdv(Instruction):
    OPCODE = 6

    def execute(self, operand, memory):
        operand = memory.combo_operand(operand)
        memory.register_b = memory.register_a >> operand
        memory.increment_instruction_pointer()


class Cdv(Instruction):
    OPCODE = 7

    def execute(self, operand, memory):
        operand = memory.combo_operand(operand)
        memory.register_c = memory.register_a >> operand
        memory.increment_instruction_pointer()


class Program:
    def __init__(self, program):
        self.program = program
        self.instruction_set = {
            inst.OPCODE: inst for inst in [Adv, Bxl, Bst, Jnz, Bxc, Out, Bdv, Cdv]
        }

    def execute_next(self, memory):
        instruction = self.instruction_set[self.program[memory.instruction_pointer]]()
        operand = self.program[memory.instruction_pointer + 1]
        instruction.execute(operand, memory)

    def execute(self, memory, output_pointer, stack):

        while memory.instruction_pointer + 1 < len(
            self.program
        ) and output_pointer >= len(memory.output):
            self.execute_next(memory)
        if memory.output == self.program and memory.instruction_pointer >= len(
            self.program
        ):
            return [memory.original_a]
        if output_pointer >= len(memory.output):
            return None
        if memory.instruction_pointer >= len(self.program):
            return None
        if self.program[: output_pointer + 1] == memory.output[: output_pointer + 1]:
            results = []
            for i in range(8):
                new_memory = copy.deepcopy(memory)
                new_memory.shift_a(i)
                result = self.execute(new_memory, output_pointer + 1, stack)
                if result:
                    results += result
            return results


def main(filename):
    with open(filename) as f:
        data = f.read()
        m = re.match(
            r"Register A: ([0-9]+)\nRegister B: ([0-9]+)\nRegister C: ([0-9]+)\n\nProgram: ([0-7,]*)",
            data,
        )
    original_memory: Memory = Memory(*(int(value) for value in m.groups()[:3]))
    program = [int(i) for i in m.groups()[3].split(",")]
    program = Program(program)
    for reg_a in range(1024):
        memory = Memory(reg_a, original_memory.register_b, original_memory.register_c)
        results = program.execute(memory, 0, [reg_a])
        if results:
            return min(results)


EXPECTED_TEST_RESULT = 117440
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
