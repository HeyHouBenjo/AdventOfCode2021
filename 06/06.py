import numpy as np


def readFish():
	with open("input") as file:
		return np.array(file.read().split(","), dtype=np.uint8)


def getCount(fish, daysLeft, usedList, usedMap):
	if daysLeft <= fish:
		return 1

	if usedList[fish][daysLeft]:
		return usedMap[(fish, daysLeft)]

	count = 1
	for d in range(0, daysLeft - fish, 7):
		count += getCount(9, daysLeft - fish - d, usedList, usedMap)

	usedList[fish][daysLeft] = True
	usedMap[(fish, daysLeft)] = count

	return count


def solve(days):

	# need to save/read known results for performance
	usedMap = {}
	usedList = np.zeros((10, days + 1), bool)

	fish = readFish()
	count = 0
	for f in fish:
		count += getCount(f, days, usedList, usedMap)

	# numpy version too slow for part 2
	# for i in range(days):
	# 	decrease = fish > 0
	# 	zeros = fish == 0
	# 	fish[decrease] -= 1
	# 	fish[zeros] = 6
	# 	fish = np.concatenate((fish, zeros[zeros].astype(np.uint8) * 8))
	# 	print(i, len(fish))

	return count


print(solve(80))
print(solve(256))

