import numpy as np


def readGrid():
	with open("input") as file:
		lines = file.read().splitlines()
		grid = np.array([[val for val in line] for line in lines], dtype=int)
	return grid


def getAdjacent(grid, x, y):
	h, w = grid.shape
	adjAdd = [
		(-1, -1),
		(-1, 0),
		(-1, 1),
		(0, 1),
		(1, 1),
		(1, 0),
		(1, -1),
		(0, -1)
	]
	adj = [(x + addX, y + addY) for addX, addY in adjAdd]
	return [(x, y) for x, y in adj if w > x >= 0 and h > y >= 0]


def solve(grid):
	flashCount = 0
	i = 0
	while True:
		i += 1
		grid += 1
		allFlashPositions = set()
		while len(grid[grid > 9]) > len(allFlashPositions):
			flashPositions = {(x, y) for y, x in np.argwhere(grid > 9)}.difference(allFlashPositions)
			for x, y in flashPositions:
				for ax, ay in getAdjacent(grid, x, y):
					grid[ay][ax] += 1
			allFlashPositions = allFlashPositions.union(flashPositions)
		for x, y in allFlashPositions:
			grid[y][x] = 0
		flashCount += len(allFlashPositions) if i <= 100 else 0
		if len(allFlashPositions) == 100:
			break

	return flashCount, i


print(solve(readGrid()))
