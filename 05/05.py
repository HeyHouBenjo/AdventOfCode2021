def readLines():
	with open("input") as file:
		lines = []
		for line in file.read().splitlines():
			p1, p2 = line.split(" -> ")
			x1, y1 = p1.split(",")
			x2, y2 = p2.split(",")
			lines.append((int(x1), int(y1), int(x2), int(y2)))
	return lines


def filterDiagonals(lines):
	new = []
	for x1, y1, x2, y2 in lines:
		if x1 == x2 or y1 == y2:
			new.append((x1, y1, x2, y2))
	return new


def expandToPointList(line):
	x1, y1, x2, y2 = line
	xDir, yDir = x2 - x1, y2 - y1
	count = max(abs(xDir), abs(yDir))
	xDir = xDir // abs(xDir) if xDir != 0 else 0
	yDir = yDir // abs(yDir) if yDir != 0 else 0
	points = []
	for i in range(count + 1):
		x, y = x1 + xDir * i, y1 + yDir * i
		points.append((x, y))
	return points


def getMostDangerousCount(lines):
	points, intersections = set(), set()
	for line in lines:
		linePoints = expandToPointList(line)
		intersections = intersections.union(points.intersection(linePoints))
		points = points.union(linePoints)
	return len(intersections)


def solve():
	allLines = readLines()
	print(getMostDangerousCount(filterDiagonals(allLines)))
	print(getMostDangerousCount(allLines))


solve()
