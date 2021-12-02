import math

values = []
with open("input", "r") as file:
	for line in file.readlines():
		values.append(int(line))

increases = 0
before = math.inf
for v in values:
	if v > before:
		increases += 1
	before = v

print(increases)

increases = 0
before = math.inf
for i in range(len(values) - 2):
	s = sum(values[i:i+3])
	if s > before:
		increases += 1
	before = s

print(increases)
