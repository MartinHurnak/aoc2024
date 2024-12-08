import os
import sys

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")


def in_map(map, y, x):
    return 0 <= y < len(map) and 0 <= x < len(map[y])


def find_antinodes(map, antenna, dist_y, dist_x):
    antinodes = set()
    i = 0
    while True:
        antinode = (antenna[0] + i * dist_y, antenna[1] + i * dist_x)
        if not in_map(map, *antinode):
            return antinodes
        antinodes.add(antinode)
        i += 1


def main(filename):
    with open(filename) as f:
        map = f.readlines()

    map = [row.strip() for row in map]

    antennas_freq = {}
    for y, row in enumerate(map):
        for x, col in enumerate(row):
            if col != ".":
                antennas_freq.setdefault(col, []).append((y, x))

    antinodes = set()
    for freq, antennas in antennas_freq.items():
        for i, antenna_1 in enumerate(antennas):
            for j, antenna_2 in enumerate(antennas[i + 1 :]):
                dist_y = antenna_1[0] - antenna_2[0]
                dist_x = antenna_1[1] - antenna_2[1]
                antinodes |= find_antinodes(
                    map, antenna_1, dist_y, dist_x
                ) | find_antinodes(map, antenna_2, -dist_y, -dist_x)
    return len(antinodes)


EXPECTED_TEST_RESULT = 34
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
