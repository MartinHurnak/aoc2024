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
        prize_x = int(prize[0].strip(",").split("=")[1]) + 10000000000000.0
        prize_y = int(prize[1].strip(",").split("=")[1]) + 10000000000000.0

        a = (prize_x * by - prize_y * bx) / (ax * by - ay * bx)
        b = (prize_x - a * ax) / bx
        if a.is_integer() and b.is_integer():
            total_tokens += 3 * a + b

    return total_tokens


EXPECTED_TEST_RESULT = 875318608908
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
