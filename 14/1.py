import os
import sys
import re
import math

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")


def main(filename, width, height):
    with open(filename) as f:
        lines = f.readlines()

    middle_x = width // 2
    middle_y = height // 2

    quadrants = [[0, 0], [0, 0]]
    for line in lines:
        robot = re.match(
            r"p=(-?[0-9]+),(-?[0-9]+) v=(-?[0-9]+),(-?[0-9]+)", line.strip()
        )
        px, py, vx, vy = (int(n) for n in robot.groups())
        px = (px + vx * TIME) % width
        py = (py + vy * TIME) % height
        if py == middle_y or px == middle_x:
            continue
        quadrants[py // (middle_y + 1)][px // (middle_x + 1)] += 1

    quadrants = [q for row in quadrants for q in row]

    return math.prod(quadrants)


TIME = 100

EXPECTED_TEST_RESULT = 12
test_and_run(
    main,
    testfile,
    EXPECTED_TEST_RESULT,
    inputfile,
    test_parameters=(11, 7),
    main_paramenters=(101, 103),
)
