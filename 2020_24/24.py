

cmdToDir = {
	"se": (0, -1),
	"nw": (0, 1),
	"sw": (-1, -1),
	"ne": (1, 1),
	"e": (1, 0),
	"w": (-1, 0)
}


def getPos(c: str):
	commands = []
	i = 0
	while i < len(c):
		if c[i] in ("s", "n"):
			commands.append(c[i:i + 2])
			i += 2
		elif c[i] in ("w", "e"):
			commands.append(c[i])
			i += 1
	x, y = 0, 0
	for command in commands:
		dx, dy = cmdToDir[command]
		x += dx
		y += dy
	return x, y


def solveTask1(codes):
	blacks = set()
	for code in codes:
		pos = getPos(code)
		if pos in blacks:
			blacks.remove(pos)
		else:
			blacks.add(pos)
	return blacks


def getAdjacent(pos):
	x, y = pos
	adjacent = [(x + dx, y + dy) for dx, dy in cmdToDir.values()]
	return set(adjacent)


def solveTask2(codes):
	blacks = solveTask1(codes)

	for _ in range(100):

		flipsToBlack, flipsToWhite = set(), set()

		for blackTile in blacks:
			adjacent = getAdjacent(blackTile)
			adjacentAndBlack = adjacent.intersection(blacks)
			if len(adjacentAndBlack) == 0 or len(adjacentAndBlack) > 2:
				flipsToWhite.add(blackTile)
			for whiteTile in adjacent.difference(blacks):
				adjacentAndBlack = getAdjacent(whiteTile).intersection(blacks)
				if len(adjacentAndBlack) == 2:
					flipsToBlack.add(whiteTile)

		blacks = blacks.difference(flipsToWhite).union(flipsToBlack)

	return blacks


with open("input") as file:
	rawCodes = file.read().splitlines()

print(len(solveTask1(rawCodes)))
print(len(solveTask2(rawCodes)))
