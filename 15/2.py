import os
import sys

sys.path.insert(0, os.getcwd())
from test_run import test_and_run, test

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
testfile3 = os.path.join(dirname, "test3.txt")
inputfile = os.path.join(dirname, "input.txt")


def in_map(map, y, x):
    return 0 <= y < len(map) and 0 <= x < len(map[y])


class Tile:
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def movable(self, map, dy, dx) -> bool:
        return True

    def move(self, map, dy, dx):
        pass

    def gps_coord(self):
        return 0


class Robot(Tile):
    def movable(self, map, dy, dx):
        if in_map(map, self.y + dy, self.x + dx):
            return map[self.y + dy][self.x + dx].movable(map, dy, dx)
        return False

    def move(self, map, dy, dx) -> bool:
        if self.movable(map, dy, dx):
            map[self.y + dy][self.x + dx].move(map, dy, dx)
            map[self.y + dy][self.x + dx] = self
            map[self.y][self.x] = Tile(self.y, self.x)
            self.y += dy
            self.x += dx


class Box(Tile):

    def movable(self, map, dy, dx) -> bool:
        if in_map(map, self.y + dy, self.x + dx) and in_map(
            map, self.y + dy, self.x + 1 + dx
        ):
            tile1 = map[self.y + dy][self.x + dx]
            tile2 = map[self.y + dy][self.x + 1 + dx]

            tile1_movable = True if tile1 is self else tile1.movable(map, dy, dx)
            # if first tile is not movable, doesn't matter id second one is
            if not tile1_movable:
                return False

            if tile2 is self:
                return True
            elif tile2 == tile1:
                return True
            else:
                return tile2.movable(map, dy, dx)

        return False

    def move(self, map, dy, dx):
        if self.movable(map, dy, dx):
            tile1 = map[self.y + dy][self.x + dx]
            tile2 = map[self.y + dy][self.x + 1 + dx]

            if tile1 is not self:
                tile1.move(map, dy, dx)
            if tile2 is not self and tile2 is not tile1:
                tile2.move(map, dy, dx)

            map[self.y][self.x] = Tile(self.y, self.x)
            map[self.y][self.x + 1] = Tile(self.y, self.x + 1)

            map[self.y + dy][self.x + dx] = self
            map[self.y + dy][self.x + 1 + dx] = self

            self.y += dy
            self.x += dx

    def gps_coord(self):
        return 100 * self.y + self.x


class Wall(Tile):
    def movable(self, map, dy, dx) -> bool:
        return False


def main(filename):
    with open(filename) as f:
        data = f.read()

    map_str, moves = data.split("\n\n")
    map_str = map_str.split("\n")
    moves = moves.replace("\n", "")

    robot = None
    map = []
    for y, row in enumerate(map_str):
        map.append([])
        for x, col in enumerate(row):
            if col == "#":
                map[y].append(Wall(y, 2 * x))
                map[y].append(Wall(y, 2 * x + 1))
            elif col == ".":
                map[y].append(Tile(y, 2 * x))
                map[y].append(Tile(y, 2 * x + 1))
            elif col == "O":
                box = Box(y, 2 * x)
                map[y].append(box)
                map[y].append(box)
            elif col == "@":
                robot = Robot(y, 2 * x)
                map[y].append(robot)
                map[y].append(Tile(y, 2 * x + 1))
            else:
                raise ValueError("Unexpected symbol on map")
    moves_dict = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
    for move in moves:
        robot.move(map, *moves_dict[move])

    boxes = set()
    for row in map:
        for tile in row:
            if isinstance(tile, Box):
                boxes.add(tile)
    return sum([box.gps_coord() for box in boxes])


# test(main, testfile3, 2028)
EXPECTED_TEST_RESULT = 9021
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
