with open("input") as file:
	startSequence = file.readline().rstrip("\n")
	file.readline()
	rulePairs = [line.split(" -> ") for line in file.read().splitlines()]
	rules = {left: right for left, right in rulePairs}


def solve(sequence):

	pairCounts, elementCounts = {}, {}

	for a, b in zip(sequence, sequence[1:]):
		pairCounts.setdefault(a + b, 0)
		pairCounts[a + b] += 1

	for a in sequence:
		elementCounts.setdefault(a, 0)
		elementCounts[a] += 1

	for i in range(40):
		for (a, b), count in pairCounts.copy().items():
			new = rules[a + b]
			elementCounts.setdefault(new, 0)
			elementCounts[new] += count
			pairCounts.setdefault(a + new, 0)
			pairCounts[a + new] += count
			pairCounts.setdefault(new + b, 0)
			pairCounts[new + b] += count
			pairCounts[a + b] -= count

	return max(elementCounts.values()) - min(elementCounts.values())


print(solve(startSequence))
