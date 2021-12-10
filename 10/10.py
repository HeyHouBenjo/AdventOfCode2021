openList = "(", "[", "{", "<"
closeList = ")", "]", "}", ">"
scores1 = 3, 57, 1197, 25137


def readLines():
	with open("input") as file:
		return file.read().splitlines()


def solve1(lines):
	counts = [0, 0, 0, 0]
	for line in lines[:]:
		stack = []
		for char in line:
			if char in openList:
				stack.append(char)
			else:
				last = stack.pop()
				closingIndex = closeList.index(char)
				valid = closingIndex == openList.index(last)
				if not valid:
					counts[closingIndex] += 1
					lines.remove(line)
					break
	return sum([s * c for s, c in zip(scores1, counts)]), lines


def solve2(lines):
	scores = []
	for line in lines:
		stack = []
		for char in line:
			stack.append(char) if char in openList else stack.pop()
		stack.reverse()
		score = 0
		for val in stack:
			score *= 5
			score += openList.index(val) + 1
		scores.append(score)
	scores.sort()
	return scores[len(scores) // 2]


task1Score, incompleteLines = solve1(readLines())
print(task1Score)
print(solve2(incompleteLines))
