import os
import re

dirname = os.path.dirname(__file__)


def test_and_run():
    test_result = main(os.path.join(dirname, "test.txt"))
    if test_result != EXPECTED_TEST_RESULT:
        print(f"Result doesn't match test, expected: {EXPECTED_TEST_RESULT}, actual")
    else:
        print("Test OK, Result:", main(os.path.join(dirname, "input.txt")))


def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    sum = 0
    for line in lines:
        for match in re.finditer(r"mul\((\d+),(\d+)\)", line):
            a, b = (int(number) for number in match.groups())
            sum += a * b
    return sum


EXPECTED_TEST_RESULT = 161
test_and_run()
