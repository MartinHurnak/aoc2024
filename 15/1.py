import os
import sys

sys.path.insert(0, os.getcwd())
from test_run import test_and_run, test

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
testfile2 = os.path.join(dirname, "test2.txt")
inputfile = os.path.join(dirname, "input.txt")


def in_map(map, y, x):
    return 0 <= y < len(map) and 0 <= x < len(map[y])


class Tile:
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def move(self, map, dy, dx) -> bool:
        return True

    def gps_coord(self):
        return 0
    
class Movable(Tile):
    def move(self, map, dy, dx) -> bool:
        if in_map(map, self.y + dy, self.x + dx):
            if map[self.y + dy][self.x + dx].move(map, dy, dx):
                map[self.y + dy][self.x + dx] = self
                map[self.y][self.x] = Tile(self.y, self.x)
                self.y += dy
                self.x += dx
                return True
        return False

class Robot(Movable):
    pass

class Box(Movable):
    def gps_coord(self):
        return 100*self.y + self.x


class Wall(Tile):
    def move(self, map, dy, dx) -> bool:
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
                map[y].append(Wall(y,x))
            elif col == ".":
                map[y].append(Tile(y, x))
            elif col == "O":
                map[y].append(Box(y,x))
            elif col == "@":
                robot = Robot(y, x)
                map[y].append(robot)
            else:
                raise ValueError("Unexpected symbol on map")
    
    moves_dict= {
        "^": (-1, 0),
        "v": (1, 0),
        "<": (0, -1),
        ">": (0, 1)
    }
    for move in moves:
        robot.move(map, *moves_dict[move])

    sum = 0
    for row in map:
        for tile in row:
            sum += tile.gps_coord()
    return sum


test(main, testfile2, 2028)
EXPECTED_TEST_RESULT = 10092
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
