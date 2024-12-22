import os
import sys

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")


def mix(secret, number):
    return secret ^ number


def prune(secret):
    return secret % 16777216


def next(secret):
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    secret = prune(mix(secret, secret * 2048))
    return secret


def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    sum = 0
    for line in lines:
        secret = int(line)
        for _ in range(2000):
            secret = next(secret)
        sum += secret

    return sum


EXPECTED_TEST_RESULT = 37327623
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
