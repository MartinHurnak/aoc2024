import os
import sys
import re
import math

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")


class Robot:
    def __init__(self, x, y, vx, vy):
        self.initial_position = (y, x)
        self.velocity = (vy, vx)

    def position(self, time, width, height):
        px = (self.initial_position[1] + self.velocity[1] * time) % width
        py = (self.initial_position[0] + self.velocity[0] * time) % height
        return py, px


def main(filename, width, height):
    # test does not make sense here
    if filename == testfile:
        return 0

    with open(filename) as f:
        lines = f.readlines()

    robots = []
    for line in lines:
        robot = re.match(
            r"p=(-?[0-9]+),(-?[0-9]+) v=(-?[0-9]+),(-?[0-9]+)", line.strip()
        )
        robots.append(Robot(*(int(n) for n in robot.groups())))

    time = 0
    while True:
        robot_positions = set([robot.position(time, width, height) for robot in robots])

        # assignment says most of the robots form the christmas tree
        # let's assume tree is symmetrical alongside y-axis
        # -> find iteration and y-axis where more than half of robots
        # are in symmetrical positions
        for x in range(width):
            symmetrical = 0
            for pos in robot_positions:
                symmetrical_position = (pos[0], x + (x - pos[1]))
                if symmetrical_position in robot_positions:
                    symmetrical += 1

            if symmetrical >= len(robot_positions) // 2:
                map = [["." for _ in range(width)] for _ in range(height)]
                for pos in robot_positions:
                    y, x = pos
                    map[y][x] = "#"
                for row in map:
                    print("".join(row))
                return time
        time += 1


EXPECTED_TEST_RESULT = 0
test_and_run(
    main,
    testfile,
    EXPECTED_TEST_RESULT,
    inputfile,
    test_parameters=(11, 7),
    main_paramenters=(101, 103),
)
