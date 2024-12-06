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


def find_unblocked_page(page_ordering):
    for page, preceding in page_ordering.items():
        if len(preceding) == 0:
            return page


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
        if not validate_page_order(rules, pages):
            page_ordering = {}
            new_page_order = []
            for page in pages:
                page_ordering[page] = [
                    rule[1] for rule in rules if rule[0] == page and rule[1] in pages
                ]
            while page_ordering:
                unblocked_page = find_unblocked_page(page_ordering)
                page_ordering.pop(unblocked_page)
                new_page_order.append(unblocked_page)
                for page, preceding in page_ordering.items():
                    preceding.remove(unblocked_page)
            sum += int(new_page_order[len(new_page_order) // 2])

    return sum


EXPECTED_TEST_RESULT = 123
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
