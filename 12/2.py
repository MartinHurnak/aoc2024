import os
import sys
import numpy as np

sys.path.insert(0, os.getcwd())
from test_run import test_and_run, test

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
testfile2 = os.path.join(dirname, "test2.txt")
testfile3 = os.path.join(dirname, "test3.txt")
testfile4 = os.path.join(dirname, "test4.txt")
inputfile = os.path.join(dirname, "input.txt")


def in_map(map, y, x):
    return 0 <= y < len(map) and 0 <= x < len(map[y])


def measure_region(garden, visited, y, x):
    visited[y][x] = True
    vertices = set()
    vertices.add((y, x))
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        edge_orientation = "H" if dy != 0 else "V"
        if not in_map(garden, y + dy, x + dx):
            continue
        elif garden[y + dy][x + dx] == garden[y][x]:
            if not visited[y + dy][x + dx]:
                vertices |= measure_region(garden, visited, y + dy, x + dx)

    return vertices


def main(filename):
    with open(filename) as f:
        garden = f.readlines()

    garden = [row.strip() for row in garden]

    visited = []
    for row in garden:
        visited_row = []
        for col in row:
            visited_row.append(False)
        visited.append(visited_row)

    fence_cost = 0
    for y, row in enumerate(garden):
        for x, col in enumerate(row):
            if not visited[y][x]:
                vertices = measure_region(garden, visited, y, x)
                area = np.zeros_like(visited)
                for vertex in vertices:
                    area[vertex] = True

                # detect which tiles are part of edges
                horizontal_edges_map = np.diff(
                    area, axis=0, prepend=False, append=False
                )
                vertical_edges_map = np.diff(area, axis=1, prepend=False, append=False)

                # edges might intersect, see test 4
                # use start and end coordinates to find intersections.
                #  if they intersect, count with 2 more edges
                yh, xh = np.where(
                    np.diff(horizontal_edges_map, axis=1, prepend=False, append=False)
                )
                horizontal_edges = set()
                for y1, y2, x1, x2 in zip(yh[::2], yh[1::2], xh[::2], xh[1::2]):
                    horizontal_edges.add((int(y1), int(x1), int(y2), int(x2)))

                xv, yv = np.where(
                    np.diff(vertical_edges_map, axis=0, prepend=False, append=False).T
                )
                vertical_edges = set()
                for y1, y2, x1, x2 in zip(yv[::2], yv[1::2], xv[::2], xv[1::2]):
                    vertical_edges.add((int(y1), int(x1), int(y2), int(x2)))

                horizontal = len(horizontal_edges)
                vertical = len(vertical_edges)
                for h in horizontal_edges:
                    for v in vertical_edges:
                        if h[1] < v[1] < h[3] and v[0] < h[0] < v[2]:
                            horizontal += 1
                            vertical += 1

                fence_cost += (horizontal + vertical) * np.sum(area)

    return fence_cost


test(main, testfile2, 80)
test(main, testfile3, 236)
test(main, testfile4, 368)
EXPECTED_TEST_RESULT = 1206
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
