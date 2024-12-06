import os

dirname = os.path.dirname(__file__)


def test_and_run():
    test_result = main(os.path.join(dirname, "test.txt"))
    if test_result != EXPECTED_TEST_RESULT:
        print(f"Result doesn't match test, expected: {EXPECTED_TEST_RESULT}, actual {test_result}")
    else:
        print("Test OK, Result:", main(os.path.join(dirname, "input.txt")))


NEEDLE = "XMAS"

def search(map, y, x, dy, dx, depth=0):
    if depth >= len(NEEDLE):
        return True
    if not 0 <= y < len(map):
        return False
    if not 0 <= x < len(map[y]):
        return False
    if map[y][x] == NEEDLE[depth]:
        return search(map, y + dy, x + dx, dy, dx, depth + 1)


def main(filename):
    with open(filename) as f:
        map = f.readlines()

    sum = 0
    for y, row in enumerate(map):
        for x, column in enumerate(row):
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if search(map, y, x, dy, dx):
                        sum += 1

    return sum

EXPECTED_TEST_RESULT = 18
test_and_run()
