from itertools import product


def readStartPositions(fileName):
	with open(fileName) as file:
		return tuple(int(line[len(line) - 1]) for line in file.read().splitlines())


def part1(p1: int, p2: int):
	P = {True: p1, False: p2}
	S = {True: 0, False: 0}
	p = True
	totalDiceCount = 0
	while True:
		diceAmount = 0
		for _ in range(3):
			diceAmount += (totalDiceCount % 100) + 1
			totalDiceCount += 1
		P[p] += diceAmount
		P[p] = ((P[p] - 1) % 10) + 1
		S[p] += P[p]
		if S[p] >= 1000:
			break
		p = not p
	print(totalDiceCount * S[not p])


cache = {}


def part2(p1, p2, s1=0, s2=0, p=True):
	if (p1, p2, s1, s2, p) in cache:
		return cache[(p1, p2, s1, s2, p)]

	winCount = {True: 0, False: 0}

	for r1, r2, r3 in product([1, 2, 3], repeat=3):
		P = {True: p1, False: p2}
		S = {True: s1, False: s2}

		P[p] += r1 + r2 + r3
		P[p] = ((P[p] - 1) % 10) + 1
		S[p] += P[p]
		if S[p] >= 21:
			winCount[p] += 1
		else:
			subWinCount = part2(*P.values(), *S.values(), not p)
			winCount[True] += subWinCount[True]
			winCount[False] += subWinCount[False]

	cache[(p1, p2, s1, s2, p)] = winCount
	return winCount


startPos = readStartPositions("input")
part1(*startPos)
print(max(part2(*startPos).values()))
