import heapq

with open("1/input.txt") as f:
    lines = f.readlines()

left, right = [], []
for line in lines:
    l, r = line.split()
    heapq.heappush(left, int(l))
    heapq.heappush(right, int(r))

sum = 0
while left and right:
    sum += abs(heapq.heappop(left) - heapq.heappop(right))
print(sum)
