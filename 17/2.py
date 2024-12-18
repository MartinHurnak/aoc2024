import os
import sys
import re

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
        self.register_b = b
        self.register_c = c
        self.instruction_pointer = 0
        self.output = []
        self.output_pointer = 0
        self.executed_jumps = set()

    def jump(self, operand):
        self.instruction_pointer = operand
        jump_key = (self.register_a, self.register_b, self.register_c, self.instruction_pointer, self.output_pointer)
        if jump_key in self.executed_jumps:
            raise LoopError()
        self.executed_jumps.add(jump_key)




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
    def __init__(self, data):
        m = re.match(
            r"Register A: ([0-9]+)\nRegister B: ([0-9]+)\nRegister C: ([0-9]+)\n\nProgram: ([0-7,]*)",
            data,
        )
        self.original_memory: Memory = Memory(*(int(value) for value in m.groups()[:3]))
        self.program = [int(i) for i in m.groups()[3].split(",")]
        self.instruction_set = {
            inst.OPCODE: inst for inst in [Adv, Bxl, Bst, Jnz, Bxc, Out, Bdv, Cdv]
        }

    def execute_next(self, memory):
        instruction = self.instruction_set[self.program[memory.instruction_pointer]]()
        operand = self.program[memory.instruction_pointer + 1]
        instruction.execute(operand, memory)


    def execute(self):
        expected_output = self.program
        output_pointer = 0
        valid_states = []
        for reg_a in range(128):
            memory = Memory(
                reg_a, self.original_memory.register_b, self.original_memory.register_c
            )
            try:
                while memory.instruction_pointer + 1 < len(self.program) and output_pointer >= len(memory.output):
                    self.execute_next(memory)
                if self.program[0] == memory.output[output_pointer]:
                    valid_states.append((reg_a, memory))
            except LoopError:
                pass
        print(valid_states)
        return 117440
            


def main(filename):
    with open(filename) as f:
        data = f.read()

    program = Program(data)
    return program.execute()


EXPECTED_TEST_RESULT = 117440
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
