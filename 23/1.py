import os
import sys

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")


def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    connections = {}
    for line in lines:
        c1, c2 = line.strip().split("-")
        connections.setdefault(c1, set()).add(c2)
        connections.setdefault(c2, set()).add(c1)

    triplets = set()
    for c1 in connections.keys():
        if not c1.startswith("t"):
            continue
        for c2 in connections[c1]:
            for c3 in connections[c1] & connections[c2]:
                triplets.add(tuple(sorted((c1, c2, c3))))

    return len(triplets)


EXPECTED_TEST_RESULT = 7
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
