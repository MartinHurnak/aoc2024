import os
import sys
import re

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")

outputs = {}
wires = {}


class Gate:
    OPERATOR = None

    def __init__(self, output_key):
        self.inputs = []
        self.output_key = output_key

    def input(self, input):
        self.inputs.append(input)
        if len(self.inputs) == 2:
            output = self.calculate_output()
            if self.output_key.startswith("z"):
                outputs[self.output_key] = output
            else:
                for gate in wires[self.output_key]:
                    gate.input(output)

    def calculate_output(self):
        raise NotImplemented


class AndGate(Gate):
    def calculate_output(self):
        return self.inputs[0] and self.inputs[1]


class OrGate(Gate):
    def calculate_output(self):
        return self.inputs[0] or self.inputs[1]


class XorGate(Gate):
    def calculate_output(self):
        return self.inputs[0] != self.inputs[1]


def main(filename):
    with open(filename) as f:
        data = f.read()

    initial_inputs, gates = data.split("\n\n")
    for gateline in gates.split("\n"):
        gate_match = re.match(r"(\w+) (AND|OR|XOR) (\w+) -> (\w+)", gateline)
        input1, operator, input2, output = gate_match.groups()
        if operator == "AND":
            gate = AndGate(output)
        elif operator == "OR":
            gate = OrGate(output)
        elif operator == "XOR":
            gate = XorGate(output)
        wires.setdefault(input1, []).append(gate)
        wires.setdefault(input2, []).append(gate)

    for inp in initial_inputs.split("\n"):
        inp_key, inp_val = inp.split(": ")
        for gate in wires[inp_key]:
            gate.input(bool(int(inp_val)))

    number = 0
    for _, bit in sorted(outputs.items(), reverse=True):
        number = 2 * number + bit
    return number


EXPECTED_TEST_RESULT = 2024
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
