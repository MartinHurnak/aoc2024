import os

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

    # TODO implement me

    return None


EXPECTED_TEST_RESULT = 0  # TODO change based on test
test_and_run()
