import numpy as np


def readGrid(fileName):
	with open(fileName) as file:
		lines = file.read().splitlines()
	grid = [list(line) for line in lines]
	return np.array(grid)


def step(herdName: str, grid: np.ndarray) -> int:
	# all places that want to move
	toMove = grid == herdName

	# complete grid shifted back one index
	gridShiftedBack = np.roll(grid, -1, 1 if herdName == ">" else 0)

	# can only move onto a dot
	toMove[gridShiftedBack != '.'] = False

	# moving objects leave a dot
	grid[toMove] = '.'

	# move objects by shifting forward on correct axis
	toMoveShiftedForward = np.roll(toMove, 1, 1 if herdName == ">" else 0)

	# set new values
	grid[toMoveShiftedForward] = herdName

	return len(grid[toMove])


def findPlace():
	grid = readGrid("input")
	count = 1
	while step('>', grid) + step('v', grid) > 0:
		count += 1
	print(count)


findPlace()
