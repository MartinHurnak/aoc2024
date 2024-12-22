import os
import sys
import numpy as np
from collections import Counter

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test2.txt")
inputfile = os.path.join(dirname, "input.txt")


def mix(secret, number):
    return secret ^ number


def prune(secret):
    return secret % 16777216


def next(secret):
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    secret = prune(mix(secret, secret * 2048))
    return secret


def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    costs = []
    for l, line in enumerate(lines):
        secret = int(line)
        costs.append([secret % 10])
        for _ in range(2000):
            secret = next(secret)
            costs[l].append(secret % 10)

    cost_diffs = np.diff(np.array(costs))

    sequence_costs = Counter()
    for r, row in enumerate(cost_diffs):
        row_costs = Counter()
        for i in range(len(row) - 3):
            seq = tuple(row[i : i + 4])
            if seq not in row_costs:
                row_costs[seq] = costs[r][i + 4]
        sequence_costs.update(row_costs)

    return sequence_costs.most_common(n=1)[0][1]


EXPECTED_TEST_RESULT = 23
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
