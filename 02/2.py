import os
from statistics import mode

dirname = os.path.dirname(__file__)


def test_and_run():
    test_result = main(os.path.join(dirname, "test.txt"))
    if test_result != EXPECTED_TEST_RESULT:
        print("Result doesn't match test, expected: {EXPECTED_TEST_RESULT}, actual")

    print("Test OK, Result:", main(os.path.join(dirname, "input.txt")))


def is_valid_increasing(delta):
    return 1 <= delta <= 3


def is_valid_decreasing(delta):
    return -3 <= delta <= -1


def report_safe(report,):
    deltas = []
    for i in range(len(report) - 1):
        deltas.append(report[i + 1] - report[i])

    if mode([delta > 0 for delta in deltas]):
        is_valid = is_valid_increasing
    else:
        is_valid = is_valid_decreasing

    invalid = []
    for i, delta in enumerate(deltas):
        if not is_valid(delta):
            invalid.append((i, i + 1))

    if len(invalid) >= 3:
        # if there are more than 3 invalid deltas, report is unfixable
        return False
    elif len(invalid) == 2:
        # if 2 deltas are not next to each other, report is unfixable
        if invalid[0][1] != invalid[1][0]:
            return False
        # if they are next to each other, try removing the number in the middle
        return is_valid(report[invalid[1][1]] - report[invalid[0][0]])
    elif len(invalid) == 1:
        # if there is just one invalid delta, we need to pick which number to remove
        upper, lower = True, True
        if (
            invalid[0][1] < len(report) - 1
        ):  # if delta is between last 2 numbers, removing last one makes report automatically valid
            upper = is_valid(report[invalid[0][1] + 1] - report[invalid[0][0]])
        if (
            invalid[0][0] > 0
        ):  # if delta is between first 2 numbers, removing first one makes report automatically valid
            lower = is_valid(report[invalid[0][1]] - report[invalid[0][0] - 1])
        return upper or lower

    return True


def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    sum = 0
    for line in lines:
        report = [int(i) for i in line.split()]
        if report_safe(report):
            sum += 1

    return sum


EXPECTED_TEST_RESULT = 4
test_and_run()
