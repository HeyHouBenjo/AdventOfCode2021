import numpy as np


def readFish():
	with open("input") as file:
		return np.array(file.read().split(","), dtype=np.uint8)


def getCount(fish, daysLeft, usedMap):
	if daysLeft <= fish:
		return 1

	if (fish, daysLeft) in usedMap:
		return usedMap[(fish, daysLeft)]

	count = 1
	for d in range(0, daysLeft - fish, 7):
		count += getCount(9, daysLeft - fish - d, usedMap)

	usedMap[(fish, daysLeft)] = count

	return count


def solve(days):

	# need to save/read known results for performance
	usedMap = {}

	fish = readFish()
	count = 0
	for f in fish:
		count += getCount(f, days, usedMap)

	return count


print(solve(80))
print(solve(256))

