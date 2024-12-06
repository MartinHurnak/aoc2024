import os
import sys

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")


def find_guard(map):
    for y, row in enumerate(map):
        for x, col in enumerate(row):
            if col in "^v<>":
                return col, y, x


class Guard:
    def __init__(self, y, x, visited):
        self.y: int = y
        self.x: int = x
        self.visited: set = visited

    def step(self):
        raise NotImplemented

    def move_guard(self, map):
        self.visited.add((self.y, self.x))

        y, x = self.step()
        if 0 <= y < len(map) and 0 <= x < len(map[y]) and map[y][x] == "#":
            return self.rotate_guard()
        else:
            self.y = y
            self.x = x
            return self

    def rotate_guard(self):
        raise NotImplemented

    @staticmethod
    def from_map(map):
        guard_type = {
            "^": NorthFacingGuard,
            "<": WestFacingGuard,
            ">": EastFacingGuard,
            "v": SouthFacingGuard,
        }
        orientation, y, x = find_guard(map)
        return guard_type[orientation](y, x, set())

    @classmethod
    def from_guard(cls, other):
        return cls(other.y, other.x, other.visited)

    def is_inside_map(self, map):
        if not 0 <= self.y < len(map):
            return False
        if not 0 <= self.x < len(map[self.y]):
            return False
        return True


class NorthFacingGuard(Guard):
    def step(self):
        return self.y - 1, self.x

    def rotate_guard(self):
        return EastFacingGuard.from_guard(self)


class WestFacingGuard(Guard):
    def step(self):
        return self.y, self.x - 1

    def rotate_guard(self):
        return NorthFacingGuard.from_guard(self)


class SouthFacingGuard(Guard):
    def step(self):
        return self.y + 1, self.x

    def rotate_guard(self):
        return WestFacingGuard.from_guard(self)


class EastFacingGuard(Guard):
    def step(self):
        return self.y, self.x + 1

    def rotate_guard(self):
        return SouthFacingGuard.from_guard(self)


def main(filename):
    with open(filename) as f:
        map = f.readlines()

    guard: Guard = Guard.from_map(map)
    while guard.is_inside_map(map):
        guard = guard.move_guard(map)
    return len(guard.visited)


EXPECTED_TEST_RESULT = 41 
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
