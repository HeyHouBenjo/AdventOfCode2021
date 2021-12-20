import numpy as np


def readInput(fileName) -> tuple[np.ndarray, np.ndarray]:
	with open(fileName) as file:
		allLines = file.read().splitlines()
	algorithm = np.fromstring(allLines[0].replace(".", "0 ").replace("#", "1 "), int, sep=" ")
	image = np.array([list(line.replace(".", "0").replace("#", "1")) for line in allLines[2:]], dtype=int)
	return algorithm, image


def apply(algorithm: np.ndarray, image: np.ndarray, fillValue: int) -> tuple[np.ndarray, int]:
	# we need to add two more elements on every side
	toReadFrom = np.pad(image, 2, constant_values=fillValue)

	# stride must contain 3x3 array of neighbour elements for each non-border element in toReadFrom (2D x 2D)
	strideSize = toReadFrom.shape[0] - 2
	strideShape = strideSize, strideSize, 3, 3
	stride = np.lib.stride_tricks.as_strided(toReadFrom, strideShape, 2 * toReadFrom.strides)

	# flatten 3x3 values
	stride = np.reshape(stride, (strideSize, strideSize, 9))

	# convert right 8 bits into decimal with np.packbits (only supports np.uint8), add 256 or 0
	codes = stride[:, :, 0] * 256 + np.packbits(stride[:, :, 1:]).reshape(strideSize, strideSize)

	newImage = algorithm[codes]

	# if fillValue is 0, take the first, if 1, take the last
	newFillValue = algorithm[fillValue * 511]

	return newImage, newFillValue


def solve():
	algorithm, startImage = readInput("input")

	# Task 1
	nextImage, newFillValue = apply(algorithm, startImage, 0)
	finalImage, _ = apply(algorithm, nextImage, newFillValue)
	print(np.count_nonzero(finalImage))

	# Task 2
	image = startImage
	fillValue = 0
	for _ in range(50):
		image, fillValue = apply(algorithm, image, fillValue)
	print(np.count_nonzero(image))


solve()
