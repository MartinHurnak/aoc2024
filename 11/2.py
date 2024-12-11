import os
import sys
import math
from functools import cache

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")


def digits(x):
    return int(math.log10(x)) + 1


# two adjacent stones never interact, stone can only split into more stones
# we can look at each stone independently and check into how many stones it will split in N blinks
@cache
def blink(stone, remaining_blinks):
    if remaining_blinks == 0:
        return 1
    if stone == 0:
        return blink(1, remaining_blinks - 1)
    stone_digits = digits(stone)
    if stone_digits % 2 == 0:
        split = 10 ** (stone_digits // 2)
        return blink(stone // split, remaining_blinks - 1) + blink(
            stone % split, remaining_blinks - 1
        )
    return blink(stone * 2024, remaining_blinks - 1)


def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    stones = [int(stone) for stone in lines[0].strip().split()]

    return sum([blink(stone, BLINKS) for stone in stones])


BLINKS = 75

EXPECTED_TEST_RESULT = 65601038650482
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
