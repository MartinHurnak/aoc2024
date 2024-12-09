import os
import sys

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")


class Block:
    def __init__(self, startpos, size):
        self.startpos = startpos
        self.size = size

    def split(self, size):
        self.size -= size

    def __lt__(self, other):
        return self.startpos > other.startpos

    def __bool__(self):
        return bool(self.size)

    def checksum(self):
        return 0


class FreeBlock(Block):
    def split(self, size):
        self.startpos += size
        super().split(size)


class FileBlock(Block):
    def __init__(self, startpos, size, id):
        super().__init__(startpos, size)
        self.id = id

    def checksum(self):
        sum = 0
        for i in range(self.startpos, self.startpos + self.size):
            sum += i * self.id
        return sum


def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    fileblocks = []
    freeblocks = []
    free = False
    id = 0
    startpos = 0
    for block in lines[0]:
        size = int(block)
        if free:
            freeblocks.append(FreeBlock(startpos, size))
        else:
            fileblocks.append(FileBlock(startpos, size, id))
            id += 1
        startpos += size
        free = not free

    freeblocks.reverse()  # to pop leftmost freeblock effectively

    checksum = 0
    first_free = None
    last_file = None
    while freeblocks:
        if not first_free:
            first_free = freeblocks.pop()
        if not last_file:
            last_file = fileblocks.pop()

        if first_free.startpos > last_file.startpos:
            checksum += last_file.checksum()
            break

        size = min(first_free.size, last_file.size)

        # we know this block won't move anymore, calculate checksum and throw it away
        checksum += FileBlock(first_free.startpos, size, last_file.id).checksum()

        first_free.split(size)
        last_file.split(size)

    return checksum + sum([block.checksum() for block in fileblocks])


EXPECTED_TEST_RESULT = 1928
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
