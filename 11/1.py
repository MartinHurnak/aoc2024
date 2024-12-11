import os
import sys
import math

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")


def digits(x):
    return int(math.log10(x)) + 1


def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    stones = [int(stone) for stone in lines[0].strip().split()]

    for _ in range(BLINKS):
        new_stones = []
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
                continue
            stone_digits = digits(stone)
            if stone_digits % 2 == 0:
                new_stones.append(stone // (10 ** (stone_digits // 2)))
                new_stones.append(stone % (10 ** (stone_digits // 2)))
                continue
            new_stones.append(stone * 2024)

        stones = new_stones

    return len(stones)


BLINKS = 25
EXPECTED_TEST_RESULT = 55312
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
