import numpy as np


def readFish():
	with open("testInput") as file:
		return np.array(file.read().split(","), dtype=np.uint8)


def getCount(fish, days):
	return 0


def solve(days):
	fish = readFish()

	count = 0
	for f in fish:
		count += getCount(f, 80)

	for i in range(0):
		decrease = fish > 0
		zeros = fish == 0
		fish[decrease] -= 1
		fish[zeros] = 6
		fish = np.concatenate((fish, zeros[zeros].astype(np.uint8) * 8))
		print(i, len(fish))

	return len(fish)


# print(solve(80))
import cProfile
cProfile.run("print(solve(200))")
