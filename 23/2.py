import os
import sys
import numpy as np

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")


# https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
def bron_kerbosh(connections, r, p, x):
    cliques = set()
    if not p and not x:
        return {tuple(sorted(r))}
    for v in p:
        cliques |= bron_kerbosh(
            connections, r | set([v]), p & connections[v], x & connections[v]
        )
        p = p - set([v])
        x = x | set([v])
    return cliques


def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    connections = {}
    for line in lines:
        c1, c2 = line.strip().split("-")
        connections.setdefault(c1, set()).add(c2)
        connections.setdefault(c2, set()).add(c1)

    cliques = bron_kerbosh(connections, set(), set(connections.keys()), set())
    best_clique = sorted(cliques, key=lambda x: -len(x))[0]
    return ",".join(best_clique)


EXPECTED_TEST_RESULT = "co,de,ka,ta"
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
