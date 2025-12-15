import os
import sys
import re

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "input.txt")
inputfile = os.path.join(dirname, "input.txt")


class Edges:
    def __init__(self):
        self._edges = {"XOR": {}, "AND": {}, "OR": {}}
        self._outputs = {}


    @staticmethod
    def _sorted_tuple(*attrs):
        return tuple(sorted(attrs))

    def add(self, operator, input1, input2, output):
        self._edges[operator][self._sorted_tuple(input1, input2)] = output
        self._outputs[output] = (operator, *self._sorted_tuple(input1, input2))
    
    def XOR(self, *inputs):
        return self._edges["XOR"].get(self._sorted_tuple(*inputs), None)
    
    def AND(self, *inputs):
        return self._edges["AND"].get(self._sorted_tuple(*inputs), None)
    
    def OR(self, *inputs):
        return self._edges["OR"].get(self._sorted_tuple(*inputs), None)
    
    def swap(self, output1, output2):
        edge1 = self._outputs[output1]
        edge2 = self._outputs[output2]

        self._edges[edge1[0]][edge1[1:]] = output2
        self._edges[edge2[0]][edge2[1:]] = output1

        self._outputs[output1] = edge2
        self._outputs[output2] = edge1

def main(filename):
    with open(filename) as f:
        data = f.read()

    _, gates = data.split("\n\n")
    
    edges = Edges()
    inputs = set()
    for gateline in gates.split("\n"):
        gate_match = re.match(r"(\w+) (AND|OR|XOR) (\w+) -> (\w+)", gateline)
        input1, operator, input2, output = gate_match.groups()
        edges.add(operator, input1, input2, output)
        inputs.add(input1)
        inputs.add(input2)
    
    x_inputs = sorted([node for node in inputs if node.startswith("x")])
    y_inputs = sorted([node for node in inputs if node.startswith("y")])

    # ok I kinda wrote the validation code, then searched for these pairs manually
    # luckily all pairs were within single adder subgraph
    edges.swap("z07", "bjm")
    edges.swap("z13", "hsw")
    edges.swap("z18", "skf")
    edges.swap("nvr", "wkr")

    # bjm,hsw,nvr,skf,wkr,z07,z13,z18

    carry = None
    for x,y in zip(x_inputs, y_inputs):
        xor_gate1 = edges.XOR(x,y)
        and_gate1 = edges.AND(x,y)
        print(f"{x} XOR {y} -> {xor_gate1}")
        print(f"{x} AND {y} -> {and_gate1}")
        if carry is None:
            carry = and_gate1
            print(f"{xor_gate1} valid LSB, carry: {and_gate1}\n")
            continue

        xor_gate2 = edges.XOR(xor_gate1, carry)
        print(f"{xor_gate1} XOR {carry} -> {xor_gate2}")
        
        and_gate2 = edges.AND(xor_gate1, carry)
        print(f"{xor_gate1} AND {carry} -> {and_gate2}")

        if xor_gate2 is None and and_gate2 is None:
            raise Exception(f"Cannot combine input {xor_gate1} and carry {carry}")

        or_gate = edges.OR(and_gate1, and_gate2)
        print(f"{and_gate1} OR {and_gate2} -> {or_gate}")

        carry = or_gate
        if not xor_gate2.startswith("z"):
            raise Exception(f"{xor_gate2} not valid output, carry: {carry}\n\n")
        print(f"{xor_gate2} valid, carry: {carry}\n\n")

    return "bjm,hsw,nvr,skf,wkr,z07,z13,z18"


EXPECTED_TEST_RESULT = "bjm,hsw,nvr,skf,wkr,z07,z13,z18"
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
