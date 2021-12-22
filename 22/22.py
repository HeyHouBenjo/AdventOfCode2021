import re
from functools import reduce


def readInstructions(fileName):
	instructions = []
	with open(fileName) as file:
		lines = file.read().splitlines()
	for line in lines:
		result = re.search(r"x=(.+)\.\.(.+),y=(.+)\.\.(.+),z=(.+)\.\.(.+)", line).groups()
		isOn = line.startswith("on")
		instructions.append((isOn, tuple(int(r) for r in result)))
	return instructions


def contains(a, b):
	ax1, ax2, ay1, ay2, az1, az2 = a
	bx1, bx2, by1, by2, bz1, bz2 = b
	return ax1 <= bx1 and ax2 >= bx2 and ay1 <= by1 and ay2 >= by2 and az1 <= bz1 and az2 >= bz2


def volume(cube):
	x1, x2, y1, y2, z1, z2 = cube
	return abs(x2 - x1) * abs(y2 - y1) * abs(z2 - z1)


def sub(a, b):
	ax1, ax2, ay1, ay2, az1, az2 = a
	bx1, bx2, by1, by2, bz1, bz2 = b

	# if currentCube contains knownCube, remove knownCube
	if contains(b, a):
		return []

	# if there are no intersections, do nothing
	if ax1 > bx2 or ax2 < bx1 or ay1 > by2 or ay2 < by1 or az1 > bz2 or az2 < bz1:
		return [a]

	xSplits = filter(lambda x: ax1 < x < ax2, [bx1, bx2])
	ySplits = filter(lambda y: ay1 < y < ay2, [by1, by2])
	zSplits = filter(lambda z: az1 < z < az2, [bz1, bz2])

	xValues = [ax1, *xSplits, ax2]
	yValues = [ay1, *ySplits, ay2]
	zValues = [az1, *zSplits, az2]

	results = []
	for i in range(len(xValues) - 1):
		for j in range(len(yValues) - 1):
			for k in range(len(zValues) - 1):
				newC = xValues[i], yValues[j], zValues[k], xValues[i + 1], yValues[j + 1], zValues[k + 1]
				if not contains(b, newC):
					results.append(newC)
	return results


def flatMap(func, elements):
	return [j for i in elements for j in func(i)]


def reboot():
	instructions = readInstructions("input")

	cubes = []

	for turnOn, coords in instructions:
		x1, x2, y1, y2, z1, z2 = coords
		currentCube = x1, x2 + 1, y1, y2 + 1, z1, z2 + 1

		cubes = flatMap(lambda c: sub(c, currentCube), cubes)

		# add to set if 'on'
		if turnOn:
			cubes.append(currentCube)

	onCount = sum(map(volume, cubes))
	print(onCount)


reboot()

# on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
# on x=967..23432,y=45373..81175,z=27513..53682