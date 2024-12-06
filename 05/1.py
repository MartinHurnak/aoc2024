import os
import sys

sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")


def validate_page_order(rules, pages):
    for i, page in enumerate(pages):
        for rule in rules:
            if page == rule[1] and rule[0] in pages[i + 1 :]:
                return False
    return True


def main(filename):
    with open(filename) as f:
        data = f.read()

    rules_str, pages_str = data.strip().split("\n\n")
    page_orders = []
    for pages_row in pages_str.split("\n"):
        page_orders.append([page for page in pages_row.split(",")])

    rules = []
    for rule_str in rules_str.split("\n"):
        rules.append(tuple(rule_str.split("|")))

    sum = 0
    for pages in page_orders:
        if validate_page_order(rules, pages):
            sum += int(pages[len(pages) // 2])

    return sum


EXPECTED_TEST_RESULT = 143
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
