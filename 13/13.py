import numpy as np

with open("input") as file:
	lines = file.read().splitlines()
	splitIndex = lines.index("")
	dotList = np.array([lines[i].split(",") for i in range(splitIndex)], dtype=int)
	col, row = dotList.T
	maxX = np.max(col)
	maxY = np.max(row)
	dotGrid = np.zeros((maxY + 1, maxX + 1), bool)
	dotGrid[row, col] = True
	foldInstructions = [lines[i].split(" ")[2].split("=") for i in range(splitIndex + 1, len(lines))]


def fold(grid, instructions: list):
	for axis, amount in instructions:
		amount = int(amount)
		if axis == "x":
			part1 = grid[:, :amount]
			part2 = grid[:, amount + 1:]
			part2Flipped = np.fliplr(part2)
		else:
			part1 = grid[:amount]
			part2 = grid[amount + 1:]
			part2Flipped = np.flipud(part2)
		grid = part1 + part2Flipped
		print(np.count_nonzero(grid))


fold(dotGrid, foldInstructions)
# Found part 2 by accident with PyCharms Array View
