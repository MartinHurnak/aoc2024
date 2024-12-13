import os
import sys

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")


def main(filename):
    with open(filename) as f:
        data = f.read()
    data = data.split("\n\n")

    total_tokens = 0
    for game in data:
        button_a, button_b, prize = game.split("\n")
        button_a = button_a.split()[2:]
        ax = int(button_a[0].strip(",").split("+")[1])
        ay = int(button_a[1].strip(",").split("+")[1])
        button_b = button_b.split()[2:]
        bx = int(button_b[0].strip(",").split("+")[1])
        by = int(button_b[1].strip(",").split("+")[1])
        prize = prize.split()[1:]
        prize_x = int(prize[0].strip(",").split("=")[1])
        prize_y = int(prize[1].strip(",").split("=")[1])

        tokens = []
        # Try lazy brute force first
        for a in range(100):
            for b in range(100):
                if a * ax + b * bx == prize_x and a * ay + b * by == prize_y:
                    tokens.append(3 * a + b)
        if tokens:
            total_tokens += min(tokens)

    return total_tokens


EXPECTED_TEST_RESULT = 480
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
