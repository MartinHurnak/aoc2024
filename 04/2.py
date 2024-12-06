import os

dirname = os.path.dirname(__file__)


def test_and_run():
    test_result = main(os.path.join(dirname, "test2.txt"))
    if test_result != EXPECTED_TEST_RESULT:
        print(
            f"Result doesn't match test, expected: {EXPECTED_TEST_RESULT}, actual {test_result}"
        )
    else:
        print("Test OK, Result:", main(os.path.join(dirname, "input.txt")))


def check_diagonal(map, y, x, dy1, dx1, dy2, dx2):
    if not 0 <= y + dy1 < len(map) or not 0 <= y + dy2 < len(map):
        return False
    if not 0 <= x + dx1 < len(map[y]) or not 0 <= x + dx2 < len(map[y]):
        return False
    if map[y + dy1][x + dx1] == "S" and map[y + dy2][x + dx2] == "M":
        return True
    if map[y + dy1][x + dx1] == "M" and map[y + dy2][x + dx2] == "S":
        return True
    return False


def main(filename):
    with open(filename) as f:
        map = f.readlines()

    sum = 0
    for y, row in enumerate(map):
        for x, column in enumerate(row):
            if column == "A":
                if check_diagonal(map, y, x, -1, -1, 1, 1) and check_diagonal(
                    map, y, x, -1, 1, 1, -1
                ):
                    sum += 1

    return sum


EXPECTED_TEST_RESULT = 9
test_and_run()
