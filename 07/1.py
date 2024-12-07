import os
import sys

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")


def validate_operators(expected, operands, tmp_result):
    if tmp_result > expected:
        # early stop optimization, cannot be fixed by applying any operator
        return False
    if len(operands) == 0:
        return tmp_result == expected
    else:
        return validate_operators(
            expected, operands[1:], tmp_result + operands[0]
        ) or validate_operators(expected, operands[1:], tmp_result * operands[0])


def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    sum = 0
    for line in lines:
        result, operands = line.split(": ")
        result = int(result)
        operands = [int(operand) for operand in operands.split()]

        if validate_operators(result, operands[1:], operands[0]):
            sum += result

    return sum


EXPECTED_TEST_RESULT = 3749
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
