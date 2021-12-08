with open("input") as file:
	lines = file.read().splitlines()
	entries = [line.split(" ") for line in lines]
	signalPatterns = [e[:10] for e in entries]
	outputValues = [e[11:] for e in entries]


def solve1():
	s = 0
	for v in outputValues:
		for digit in v:
			if len(digit) in (2, 4, 3, 7):
				s += 1
	return s


def find(iterable, cond):
	if isinstance(iterable, dict):
		for k, v in iterable.items():
			if cond(k, v):
				return k, v
	else:
		for element in iterable:
			if cond(element):
				return element
	return None


def solve2():
	s = 0
	for unorderedPatterns, output in zip(signalPatterns, outputValues):
		patterns = [set(letter) for letter in unorderedPatterns]
		digits = {
			1: find(patterns, lambda x: len(x) == 2),
			4: find(patterns, lambda x: len(x) == 4),
			7: find(patterns, lambda x: len(x) == 3),
			8: find(patterns, lambda x: len(x) == 7)
		}

		# 5 segments: 2, 3, 5
		# 6 segments: 0, 6, 9

		# 3 is superset of 1 while 2 and 5 are not
		digits[3] = find(patterns, lambda x: len(x) == 5 and x > digits[1])

		# 9 is superset of 3 while 0 and 6 are not
		digits[9] = find(patterns, lambda x: len(x) == 6 and x > digits[3])

		# 0 is superset of 1, but 9 is also, so exclude it
		digits[0] = find(patterns, lambda x: len(x) == 6 and x > digits[1] and x != digits[9])

		# 6 is the last 6-segment digit
		digits[6] = find(patterns, lambda x: len(x) == 6 and x not in (digits[0], digits[9]))

		# 5 is a subset of 6, while 2 and 1 are not
		digits[5] = find(patterns, lambda x: len(x) == 5 and x < digits[6])

		# 2 is the very last one
		digits[2] = find(patterns, lambda x: x not in digits.values())

		outputSets = [set(letters) for letters in output]
		number = 0
		for out in outputSets:
			number = number * 10 + find(digits, lambda _, d: out == d)[0]
		s += number
	return s


print(solve1())
print(solve2())
