import re


def readInstructions(fileName):
	instructions = []
	with open(fileName) as file:
		lines = file.read().splitlines()
	for line in lines:
		result = re.search(r"x=(.+)\.\.(.+),y=(.+)\.\.(.+),z=(.+)\.\.(.+)", line).groups()
		sign = 1 if line.startswith("on") else -1
		result = tuple((sign,)) + tuple(result)
		instructions.append(tuple(int(r) for r in result))
	return instructions


def volume(cube):
	sign, x1, x2, y1, y2, z1, z2 = cube
	return (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1) * sign


def intersect(a, b):
	_, ax1, ax2, ay1, ay2, az1, az2 = a
	bSign, bx1, bx2, by1, by2, bz1, bz2 = b
	if ax1 > bx2 or ax2 < bx1 or ay1 > by2 or ay2 < by1 or az1 > bz2 or az2 < bz1:
		return None

	x1 = max(ax1, bx1)
	x2 = min(ax2, bx2)
	y1 = max(ay1, by1)
	y2 = min(ay2, by2)
	z1 = max(az1, bz1)
	z2 = min(az2, bz2)

	sign = -bSign

	return sign, x1, x2, y1, y2, z1, z2


def reboot():
	instructions = readInstructions("input")

	cubes = []

	for currentCube in instructions:

		for cube in cubes.copy():
			if intersection := intersect(currentCube, cube):
				cubes.append(intersection)

		if currentCube[0] == 1:
			cubes.append(currentCube)

	filteredCubes = filter(lambda c: -50 <= c[1] <= 50, cubes)
	print(sum(map(lambda c: volume(c), filteredCubes)))
	print(sum(map(lambda c: volume(c), cubes)))


reboot()
