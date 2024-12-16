import os
import sys
import math
import heapq
import numpy as np

sys.path.insert(0, os.getcwd())
from test_run import test_and_run, test

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
testfile2 = os.path.join(dirname, "test2.txt")
inputfile = os.path.join(dirname, "input.txt")


def get_node(map, y, x):
    if 0 <= y < len(map) and 0 <= x < len(map[y]):
        if map[y][x]:
            return y, x
    return None


class Node:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.cost = math.inf
        self.previous = None

    def __lt__(self, other):
        return self.cost < other.cost

    def update_neighbours(self, map, pq, visited, previous):
        key = (self.y, self.x, previous.y, previous.x)
        visited.add(key)
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbour = get_node(map, self.y + dy, self.x + dx)
            if neighbour and not (*neighbour, self.y, self.x) in visited:
                if dy == self.y - previous.y and dx == self.x - previous.x:
                    step = 1
                elif -dy == self.y - previous.y and -dx == self.x - previous.x:
                    continue
                else:
                    step = 1001

                node = Node(*neighbour)
                node.cost = self.cost + step
                node.previous = self
                pq.push(node)


class PriorityQueue:
    def __init__(self, map):
        self.map = map
        self.queue = []

    def push(self, item: Node):
        heapq.heappush(self.queue, item)

    def pop(self):
        return heapq.heappop(self.queue)

    def __bool__(self):
        return bool(self.queue)


def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    map = []
    queue = PriorityQueue(map)
    visited = set()
    for y, row in enumerate(lines):
        map.append([])
        for x, col in enumerate(row.strip()):
            if col == "#":
                map[y].append(False)
                continue

            if col == "S":
                start = node = (y, x)
            elif col == "E":
                end = node = (y, x)
            elif col == ".":
                node = (y, x)
            map[y].append(True)

    pq_item = Node(*start)
    pq_item.cost = 0
    pq_item.previous = Node(start[0], start[1] - 1)
    queue.push(pq_item)

    shortest_paths = np.zeros_like(map, dtype=np.int32)

    path_length = math.inf
    while queue:
        pq_item = queue.pop()
        if pq_item.cost > path_length:
            break
        if (pq_item.y, pq_item.x) == end:
            path_length = pq_item.cost
            n = pq_item
            while True:
                shortest_paths[n.y][n.x] = True
                if (n.y, n.x) == start:
                    break
                n = n.previous

        else:
            pq_item.update_neighbours(map, queue, visited, pq_item.previous)

    return np.sum(shortest_paths)

test(main, testfile2, 64)
EXPECTED_TEST_RESULT = 45
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
