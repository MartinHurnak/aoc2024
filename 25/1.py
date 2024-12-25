import os
import sys
import numpy as np

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")


def main(filename):
    with open(filename) as f:
        data = f.read()

    locks, keys = [], []
    for entry in data.split("\n\n"):
        heights = np.zeros((5,))
        for line in entry.split("\n"):
            for i, col in enumerate(line):
                if col == "#":
                    heights[i] += 1
        heights -= 1
        if entry.startswith("#####\n"):
            locks.append(heights)
        else:
            keys.append(heights)

    sum = 0
    for lock in locks:
        for key in keys:
            if ((key + lock) <= 5).all():
                sum += 1

    return sum


EXPECTED_TEST_RESULT = 3
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
