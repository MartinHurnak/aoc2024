import os
import sys
import re
import functools

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

    @functools.cache
    def match_design(design):
        if design == "":
            return 1
        available = 0
        for towel in towels:
            if design.startswith(towel):
                available += match_design(design[len(towel) :])
        return available

    available = 0
    for design in designs:
        available += match_design(design)

    return available


EXPECTED_TEST_RESULT = 16
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
