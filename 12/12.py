
with open("input") as file:
	lines = file.read().splitlines()
	edges = [set(line.split("-")) for line in lines]


def getAdjacent(knot: str) -> set[str]:
	return {edge.difference({knot}).pop() for edge in edges if knot in edge}


def solve():

	def find(knot: str, visited: set[str], smallUsedTwice: bool) -> set[tuple[str, ...]]:
		if knot == "end":
			return {"end"}
		foundPaths = set()
		newVisited = visited.union({knot}) if knot.islower() else visited
		for k in getAdjacent(knot).difference(visited):
			if knot.islower() and not smallUsedTwice and knot != "start":
				for p in find(k, visited, True):
					foundPaths.add((knot, *p))
			for p in find(k, newVisited, smallUsedTwice):
				foundPaths.add((knot, *p))
		return foundPaths

	paths1 = find("start", set(), True)
	paths2 = find("start", set(), False)

	print(len(paths1), len(paths2))


solve()
