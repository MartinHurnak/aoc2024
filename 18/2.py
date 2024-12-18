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
    trace = {}
    while queue:
        current = queue.popleft()

        if current[0] == end:
            return reconstruct_path(trace, start, end)
        y, x = current[0]

        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if in_map(map, y + dy, x + dx) and (y + dy, x + dx) not in trace:
                queue.append(((y + dy, x + dx), current[1] + 1))
                trace[y + dy, x + dx] = (y, x)

    return None


def reconstruct_path(trace, start, end):
    current = end
    path = []
    while current != start:
        path.append(current)
        current = trace[current]
    return path


def main(filename, width, height, n_bytes):
    with open(filename) as f:
        lines = f.readlines()

    end = (0, 0)
    start = (width - 1, height - 1)

    map = [[True] * width for _ in range(height)]
    for line in lines[:n_bytes]:
        x, y = (int(i) for i in line.split(","))
        map[y][x] = False

    path = bfs(map, start, end)
    for line in lines[n_bytes:]:
        x, y = (int(i) for i in line.split(","))
        map[y][x] = False
        if (y, x) in path:
            path = bfs(map, start, end)
        if path is None:
            return line.strip()


EXPECTED_TEST_RESULT = "6,1"
test_and_run(
    main,
    testfile,
    EXPECTED_TEST_RESULT,
    inputfile,
    test_parameters=(7, 7, 12),
    main_paramenters=(71, 71, 1024),
)
