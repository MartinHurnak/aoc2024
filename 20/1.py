import os
import sys
from collections import deque
import numpy as np

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")


def in_map(map, y, x):
    return 0 <= y < len(map) and 0 <= x < len(map[y])


def bfs(map, start, end):
    queue = deque()
    queue.append(end)
    lengths = np.full_like(map, np.inf, dtype=np.float64)
    lengths[end] = 0
    while queue:
        y, x = queue.popleft()
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if (
                in_map(map, y + dy, x + dx)
                and map[y + dy][x + dx]
                and np.isinf(lengths[y + dy][x + dx])
            ):
                lengths[y + dy][x + dx] = lengths[y][x] + 1
                queue.append((y + dy, x + dx))
    return lengths


def main(filename, min_cheat):
    with open(filename) as f:
        lines = f.readlines()
    lines = [list(line.strip()) for line in lines]
    map = np.zeros_like(lines, dtype=np.int64)
    for y, row in enumerate(lines):
        for x, col in enumerate(row):
            if col == "#":
                map[y][x] = False
                continue
            if col == "S":
                start = (y, x)
            elif col == "E":
                end = (y, x)
            map[y][x] = True
    pathmap = bfs(map, start, end)
    print(pathmap)

    vertical_cheats = np.abs(pathmap[:-2] - pathmap[2:]) - 2
    horizontal_cheats = np.abs(pathmap[:, :-2] - pathmap[:, 2:]) - 2

    horizontal_best = horizontal_cheats[
        (horizontal_cheats >= min_cheat) & ~np.isinf(horizontal_cheats)
    ]
    vertical_best = vertical_cheats[
        (vertical_cheats >= min_cheat) & ~np.isinf(vertical_cheats)
    ]
    return len(horizontal_best) + len(vertical_best)


EXPECTED_TEST_RESULT = 4
test_and_run(
    main,
    testfile,
    EXPECTED_TEST_RESULT,
    inputfile,
    test_parameters=(36,),
    main_paramenters=(100,),
)
