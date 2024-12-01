from collections import Counter


with open("1/input.txt") as f:
    lines = f.readlines()

left = Counter()
right = Counter()
for line in lines:
    l, r = line.split()
    left[int(l)] += 1
    right[int(r)] += 1

sum = 0
for l, l_count in left.items():
    sum += l * l_count * right[l]
print(sum)
