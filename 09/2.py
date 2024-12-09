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

    checksum = 0
    for fileblock in reversed(fileblocks):
        freeblock_index = next(
            (
                index
                for index, block in enumerate(freeblocks)
                if block.size >= fileblock.size and block.startpos < fileblock.startpos
            ),
            None,
        )
        if freeblock_index is not None:
            fileblock.startpos = freeblocks[freeblock_index].startpos
            freeblocks[freeblock_index].split(fileblock.size)
        checksum += fileblock.checksum()

    return checksum


EXPECTED_TEST_RESULT = 2858
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
