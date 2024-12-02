with open("2/input.txt") as f:
    lines = f.readlines()


def report_safe(report):
    increasing = (report[1] - report[0]) > 0
    for i in range(len(report) - 1):
        delta = report[i + 1] - report[i]
        if increasing and not 1 <= delta <= 3:
            return False
        if not increasing and not -3 <= delta <= -1:
            return False

    return True


sum = 0
for line in lines:
    if report_safe([int(i) for i in line.split()]):
        sum += 1

print(sum)
