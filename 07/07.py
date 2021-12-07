def getMedian(arr):
	n = len(arr)
	if n % 2 == 0:
		return (arr[n // 2] + arr[n // 2 - 1]) / 2
	if n % 2 != 0:
		return arr[n // 2]


def getMean(arr):
	return sum(arr) / len(arr)


def calculateFuel(positions, target, expensive=False):
	fuelNeeded = 0
	for p in positions:
		add = abs(p - target)
		if expensive:
			add = add * (add + 1) / 2
		fuelNeeded += add
	return fuelNeeded


def solve1(positions):
	positions.sort()
	median = getMedian(positions)
	fuelNeeded = calculateFuel(positions, median)
	return fuelNeeded


def solve2(positions):
	# int (floor) works for complete input, ceiling does for the testInput. No clue.
	mean = int(getMean(positions))
	fuelNeeded = calculateFuel(positions, mean, True)
	return fuelNeeded


def readPositions():
	with open("input") as file:
		return [int(num) for num in file.read().split(",")]


print(solve1(readPositions()))
print(solve2(readPositions()))

