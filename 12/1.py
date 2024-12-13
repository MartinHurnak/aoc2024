import os
import sys

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")


def in_map(map, y, x):
    return 0 <= y < len(map) and 0 <= x < len(map[y])


def measure_region(garden, visited, y, x):
    visited[y][x] = True
    area, perimeter = 1, 0
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        if not in_map(garden, y + dy, x + dx):
            perimeter += 1
        elif garden[y + dy][x + dx] == garden[y][x]:
            if not visited[y + dy][x + dx]:
                new_area, new_perimeter = measure_region(
                    garden, visited, y + dy, x + dx
                )
                area += new_area
                perimeter += new_perimeter
        else:
            perimeter += 1

    return area, perimeter


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
                area, perimeter = measure_region(garden, visited, y, x)
                print(f"Region {garden[y][x]}: {area} * {perimeter} = {area*perimeter}")
                fence_cost += area * perimeter

    return fence_cost


EXPECTED_TEST_RESULT = 1930
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
