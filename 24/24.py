# Code translated from https://github.com/Mahrgell/AoC2021/blob/main/aoc21-24/src/main.rs


def readMonad(fileName):
	with open(fileName) as file:
		lines = file.read().splitlines()
	instructions: list[tuple[str, tuple[str, ...]]] = []
	for line in lines:
		instrValues = tuple(line.split(" "))
		append = (instrValues[0], instrValues[1:])
		instructions.append(append)
	return instructions


fieldToPos = {
	'x': 0,
	'y': 1,
	'z': 2,
	'w': 3
}

calc = {
	'add': lambda a, b: a + b,
	'mul': lambda a, b: a * b,
	'div': lambda a, b: a // b,
	'mod': lambda a, b: a % b,
	'eql': lambda a, b: 1 if a == b else 0
}


def find():
	instructions = readMonad("input")
	states: list[tuple[list[int], tuple[int, int]]] = [([0, 0, 0, 0], (0, 0))]
	i = 1
	for cmd, values in instructions:
		if cmd == "inp":
			newStates = []
			knownAluIndices = {}
			field = values[0]
			for alu, (minV, maxV) in states:
				for v in range(1, 10):
					newAlu = alu.copy()
					newAlu[fieldToPos[field]] = v
					minV, maxV = minV * 10 + v, maxV * 10 + v
					if index := knownAluIndices.get(tuple(newAlu)):
						alu, (newMin, newMax) = newStates[index]
						newMin = min(newMin, minV)
						newMax = max(newMax, maxV)
						newStates[index] = alu, (newMin, newMax)
					else:
						knownAluIndices[tuple(newAlu)] = len(newStates)
						newStates.append((newAlu, (minV, maxV)))
			states = newStates
			print(f"{i} Processing {len(states)} states")
			i += 1
		else:
			for alu, _ in states:
				field1, field2 = values
				v2 = int(field2) if field2.lstrip("-").isnumeric() else alu[fieldToPos[field2]]
				pos1 = fieldToPos[field1]
				alu[pos1] = calc[cmd](alu[pos1], v2)

	valid = {minmax for alu, minmax in states if alu[3] == 0}
	lowest = min(m for m, _ in valid)
	highest = max(m for _, m in valid)
	print(lowest, highest)


find()
