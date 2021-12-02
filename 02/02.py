
actions = []

with open("input", "r") as file:
	for raw in file.read().splitlines():
		cmd, amount = raw.split(" ")
		actions.append((cmd, int(amount)))

x, depth = 0, 0
for cmd, amount in actions:
	if cmd == "forward":
		x += amount
	if cmd == "up":
		depth -= amount
	if cmd == "down":
		depth += amount

print(f"Horizontal: {x}")
print(f"Depth: {depth}")
print(x * depth)


x, depth, aim = 0, 0, 0
for cmd, amount in actions:
	if cmd == "forward":
		x += amount
		depth += aim * amount
	if cmd == "up":
		aim -= amount
	if cmd == "down":
		aim += amount

print(f"Horizontal: {x}")
print(f"Depth: {depth}")
print(x * depth)
