import os
import sys
from collections import deque

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")


def in_map(map, y, x):
    if 0 <= y < len(map) and 0 <= x < len(map[y]):
        return map[y][x]
    return False


def bfs(map, start, end):
    queue = deque()
    queue.append((start, 0))
    visited = set()
    while True:
        current = queue.popleft()

        if current[0] == end:
            return current[1]
        y, x = current[0]

        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if in_map(map, y + dy, x + dx) and (y + dy, x + dx) not in visited:
                queue.append(((y + dy, x + dx), current[1] + 1))
                visited.add((y + dy, x + dx))


def main(filename, width, height, bytes):
    with open(filename) as f:
        lines = f.readlines()

    map = [[True] * width for _ in range(height)]
    for line in lines[:bytes]:
        x, y = (int(i) for i in line.split(","))
        map[y][x] = False

    end = (0, 0)
    start = (width - 1, height - 1)
    return bfs(map, start, end)


EXPECTED_TEST_RESULT = 22
test_and_run(
    main,
    testfile,
    EXPECTED_TEST_RESULT,
    inputfile,
    test_parameters=(7, 7, 12),
    main_paramenters=(71, 71, 1024),
)
