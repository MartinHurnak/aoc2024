import os
import sys
import re

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")


def main(filename):
    with open(filename) as f:
        data = f.read()

    towels, designs = data.split("\n\n")
    towels = towels.strip().split(", ")
    designs = designs.split("\n")
    pattern = re.compile(f"({'|'.join(towels)})*")
    available = 0
    for design in designs:
        if pattern.fullmatch(design):
            available += 1

    return available


EXPECTED_TEST_RESULT = 6
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
