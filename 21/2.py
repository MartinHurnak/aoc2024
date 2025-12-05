import os
import sys
import numpy as np
from collections import Counter

sys.path.insert(0, os.getcwd())
from test_run import test_and_run, test

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
testfile2 = os.path.join(dirname, "test2.txt")
testfile3 = os.path.join(dirname, "test3.txt")
inputfile = os.path.join(dirname, "input.txt")


class Keyboard:
    def __init__(self, shape, tiles, keyboard):
        self._keyboard = {}
        self._reverse_keyboard = {}
        for y in range(shape[0]):
            for x in range(shape[1]):
                self._keyboard[tiles[y * shape[1] + x]] = np.array([y, x])
                self._reverse_keyboard[tuple(np.array([y, x]))] = tiles[
                    y * shape[1] + x
                ]
        self.current = self._keyboard["A"].copy()
        self.indirect_keyboard = keyboard

        self.cache = {}

    def calculate_move(self, tile):
        return self._keyboard[tile] - self.current

    def generate_move_sequence(self, code):
        moves = [self.generate_moves(c) for c in code]
        key = (code, "".join(moves))
        if key in self.cache:
            return self.cache[key]
    
        if not self.indirect_keyboard:
            self.cache[key] = len(code)
            return len(code)


        sequence = 0
        for m in moves:
            sequence += self.indirect_keyboard.generate_move_sequence(m)
        if key in self.cache and self.cache[key] != sequence:
            raise Exception("bam")
        self.cache[key] = sequence
        return sequence

    def generate_moves(self, key):
        sequence = ""
        move = self.calculate_move(key)
        if self._reverse_keyboard[tuple(self.current + np.array([0, move[1]]))] is None:
            if move[0] < 0:
                sequence += "^" * abs(move[0])
                self.current[0] += move[0]
                move[0] = 0
            if move[0] > 0:
                sequence += "v" * abs(move[0])
                self.current[0] += move[0]
                move[0] = 0
        if move[1] < 0:
            sequence += "<" * abs(move[1])

        if self._reverse_keyboard[tuple(self.current + np.array([move[0], 0]))] is None:
            if move[1] > 0:
                sequence += ">" * abs(move[1])
                self.current[1] += move[1]
                move[1] = 0

        if move[0] > 0:
            sequence += "v" * abs(move[0])

        if move[0] < 0:
            sequence += "^" * abs(move[0])
        if move[1] > 0:
            sequence += ">" * abs(move[1])

        sequence += "A"

        self.current += move
        return sequence


def main(filename, indirect_keyboards):
    with open(filename) as f:
        lines = f.readlines()

    sum = 0
    codes = [line.strip() for line in lines]
    for code in codes:
        
        keyboards = [Keyboard((2, 3), [None, "^", "A", "<", "v", ">"], None)]

        for _ in range(indirect_keyboards):
            keyboards.append(
                Keyboard((2, 3), [None, "^", "A", "<", "v", ">"], keyboards[-1])
            )

        keyboards.append(
            Keyboard(
                (4, 3),
                ["7", "8", "9", "4", "5", "6", "1", "2", "3", None, "0", "A"],
                keyboards[-1],
            )
        )

        sequence_len = keyboards[-1].generate_move_sequence(code)
        sum += int(code.strip("A")) * sequence_len
    return sum



test(main, testfile2, 984, test_parameters=(4,))
test(main, testfile, 154115708116294, test_parameters=(25,))
# test(main, testfile3, 328, test_parameters=(1,))
EXPECTED_TEST_RESULT = 126384
test_and_run(
    main,
    testfile,
    EXPECTED_TEST_RESULT,
    inputfile,
    test_parameters=(2,),
    main_paramenters=(25,),
)

