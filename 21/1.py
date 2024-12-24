import os
import sys
import numpy as np

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")


class Keyboard:
    def __init__(self, shape, tiles):
        self._keyboard = {}
        self._reverse_keyboard = {}
        for y in range(shape[0]):
            for x in range(shape[1]):
                self._keyboard[tiles[y * shape[1] + x]] = np.array([y, x])
                self._reverse_keyboard[tuple(np.array([y, x]))] = tiles[
                    y * shape[1] + x
                ]
        self.current = self._keyboard["A"].copy()

    def calculate_move(self, tile):
        return self._keyboard[tile] - self.current

    def generate_move_sequence(self, code):
        sequence = []
        for c in code:
            move = self.calculate_move(c)
            if (
                self._reverse_keyboard[tuple(self.current + np.array([0, move[1]]))]
                is None
            ):
                if move[0] < 0:
                    sequence += ["^"] * abs(move[0])
                    self.current[0] += move[0]
                    move[0] = 0
                if move[0] > 0:
                    sequence += ["v"] * abs(move[0])
                    self.current[0] += move[0]
                    move[0] = 0
            if move[1] < 0:
                sequence += ["<"] * abs(move[1])
            if move[0] > 0:
                sequence += ["v"] * abs(move[0])
            if move[1] > 0:
                sequence += [">"] * abs(move[1])
            if move[0] < 0:
                sequence += ["^"] * abs(move[0])

            sequence.append("A")
            self.current += move
        return sequence


def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    keyboards = [
        Keyboard((4, 3), ["7", "8", "9", "4", "5", "6", "1", "2", "3", None, "0", "A"]),
        Keyboard((2, 3), [None, "^", "A", "<", "v", ">"]),
        Keyboard((2, 3), [None, "^", "A", "<", "v", ">"]),
    ]
    sum = 0
    codes = [line.strip() for line in lines]
    for code in codes:
        sequence = code
        for keyboard in keyboards:
            sequence = keyboard.generate_move_sequence(sequence)
        sum += int(code.strip("A")) * len(sequence)
    return sum


EXPECTED_TEST_RESULT = 126384
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
