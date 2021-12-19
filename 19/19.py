from itertools import combinations


def readInput(fileName):
	scanners = []
	with open(fileName) as file:
		lines = file.read().splitlines()
	for line in lines:
		if line == "":
			continue
		if line.startswith("---"):
			scanners.append(set())
			continue
		scanners[len(scanners) - 1].add(tuple(int(value) for value in line.split(",")))
	return scanners


Point = tuple[int, int, int]
axes = {(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)}


def transform(p: Point, up: Point, rotation: int):
	new = {
		(1, 0, 0): (p[1], p[0], -p[2]),
		(-1, 0, 0): (p[1], -p[0], p[2]),
		(0, 1, 0): p,
		(0, -1, 0): (p[0], -p[1], -p[2]),
		(0, 0, 1): (p[1], p[2], p[0]),
		(0, 0, -1): (p[1], -p[2], -p[0])
	}[up]
	return {
		0: new,
		1: (new[2], new[1], -new[0]),
		2: (-new[0], new[1], -new[2]),
		3: (-new[2], new[1], new[0])
	}[rotation]


def add(p1: Point, p2: Point):
	return tuple(val1 + val2 for val1, val2 in zip(p1, p2))


def sub(p1: Point, p2: Point):
	return tuple(val1 - val2 for val1, val2 in zip(p1, p2))


def align(beacons1: set[Point], beacons2: set[Point]):
	for axis in axes:
		for rotation in range(4):
			rotatedBeacons2 = set(transform(p, axis, rotation) for p in beacons2)
			for b1 in beacons1:
				for maybeMatchingInB2 in rotatedBeacons2:
					delta = sub(b1, maybeMatchingInB2)
					transformedBeacons2 = set(add(p, delta) for p in rotatedBeacons2)
					if len(transformedBeacons2.intersection(beacons1)) >= 12:
						return transformedBeacons2, delta, axis, rotation
	return None


def reduce(scans: list[set[Point]], scanners: list[set[Point]]):
	toRemove = set()
	for i in range(len(scans) - 1):
		for j in range(i + 1, len(scans)):
			if j in toRemove:
				continue
			alignment = align(scans[i], scans[j])
			if alignment is not None:
				alignedBeacons, translation, up, rotation = alignment
				for scan in scanners[j]:
					scanners[i].add(add(translation, transform(scan, up, rotation)))
				scans[i] |= alignedBeacons
				toRemove.add(j)
	return [s for i, s in enumerate(scans) if i not in toRemove], [s for i, s in enumerate(scanners) if i not in toRemove]


def solve():
	scans = readInput("input")
	scanners = [{(0, 0, 0)} for _ in scans]
	while len(scans) > 1:
		scans, scanners = reduce(scans, scanners)
	allBeacons = scans[0]
	print(len(allBeacons))
	print(max(abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2) for (x1, y1, z1), (x2, y2, z2) in combinations(scanners[0], 2)))


solve()
