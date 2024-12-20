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


def bfs(map, start, maxdepth=None):
    queue = deque()
    queue.append(start)
    distances = np.full_like(map, np.inf, dtype=np.float64)
    distances[start] = 0
    while queue:
        y, x = queue.popleft()
        if maxdepth and distances[(y, x)] >= maxdepth:
            break
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if (
                in_map(map, y + dy, x + dx)
                and map[y + dy][x + dx]
                and np.isinf(distances[y + dy][x + dx])
            ):
                distances[(y + dy, x + dx)] = distances[(y, x)] + 1
                queue.append((y + dy, x + dx))
    return distances


MAX_CHEAT_DIST = 20


def main(filename, min_cheat):
    with open(filename) as f:
        lines = f.readlines()
    lines = [list(line.strip()) for line in lines]
    map = np.zeros_like(lines, dtype=np.bool)
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
    track_points = bfs(map, end)
    track_points = np.where(map, track_points, np.inf)

    cheats = 0
    manhattan_distances = np.sum(
        np.abs(np.indices((2 * MAX_CHEAT_DIST + 1, 2 * MAX_CHEAT_DIST + 1)) - MAX_CHEAT_DIST), axis=0
    )
    manhattan_distances = np.where(
        manhattan_distances > MAX_CHEAT_DIST, np.inf, manhattan_distances
    )

    for trackpoint in np.argwhere(map):
        y, x = trackpoint = tuple(trackpoint)
        selection = track_points[
            max(0, y - MAX_CHEAT_DIST) : y + MAX_CHEAT_DIST + 1,
            max(0, x - MAX_CHEAT_DIST) : x + MAX_CHEAT_DIST + 1,
        ]
        cheat_distances = manhattan_distances[
            max(0, MAX_CHEAT_DIST - y) : MAX_CHEAT_DIST + min(map.shape[0] - y, MAX_CHEAT_DIST + 1),
            max(0, MAX_CHEAT_DIST - x) : MAX_CHEAT_DIST + min(map.shape[1] - x, MAX_CHEAT_DIST + 1),
        ]
        possible_cheats = track_points[y, x] - (selection + cheat_distances)

        cheats += np.sum(possible_cheats >= min_cheat)

    return cheats


EXPECTED_TEST_RESULT = 285
test_and_run(
    main,
    testfile,
    EXPECTED_TEST_RESULT,
    inputfile,
    test_parameters=(50,),
    main_paramenters=(100,),
)
