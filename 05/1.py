import os
from test import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")

def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    # TODO implement me

    return None


EXPECTED_TEST_RESULT = 0  # TODO change based on test
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
