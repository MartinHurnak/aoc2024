import os
import sys

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")


def in_map(map, y, x):
    return 0 <= y < len(map) and 0 <= x < len(map[y])


def peaks_dfs(map, y, x):
    if map[y][x] == 9:
        return set([(y, x)])

    peaks = set()
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if in_map(map, y + dy, x + dx):
            if map[y + dy][x + dx] == map[y][x] + 1:
                peaks |= peaks_dfs(map, y + dy, x + dx)
    return peaks


def main(filename):
    with open(filename) as f:
        map = f.readlines()

    map = [list(int(col) for col in row.strip()) for row in map]

    score = 0
    for y, row in enumerate(map):
        for x, col in enumerate(row):
            if col == 0:
                score += len(peaks_dfs(map, y, x))
    return score


EXPECTED_TEST_RESULT = 36
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
