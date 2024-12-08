import os
import sys

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")


def in_map(map, y, x):
    return 0 <= y < len(map) and 0 <= x < len(map[y])


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
                antinode_1 = (antenna_1[0] + dist_y, antenna_1[1] + dist_x)
                antinode_2 = (antenna_2[0] - dist_y, antenna_2[1] - dist_x)
                if in_map(map, *antinode_1):
                    antinodes.add(antinode_1)
                    print(freq, antenna_1, antenna_2, antinode_1)
                if in_map(map, *antinode_2):
                    antinodes.add(antinode_2)
                    print(freq, antenna_1, antenna_2, antinode_2)

    return len(antinodes)


EXPECTED_TEST_RESULT = 14  # TODO change based on test
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
import os
import sys

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")


def in_map(map, y, x):
    return 0 <= y < len(map) and 0 <= x < len(map[y])


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
                antinode_1 = (antenna_1[0] + dist_y, antenna_1[1] + dist_x)
                antinode_2 = (antenna_2[0] - dist_y, antenna_2[1] - dist_x)
                if in_map(map, *antinode_1):
                    antinodes.add(antinode_1)
                if in_map(map, *antinode_2):
                    antinodes.add(antinode_2)

    return len(antinodes)


EXPECTED_TEST_RESULT = 14
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
