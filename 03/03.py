with open("input", "r") as file:
	data = file.read().splitlines()


def binaryToDecimal(binArray):
	base = 2
	result = 0
	for position in range(len(binArray)):
		exp = len(binArray) - position - 1
		result += binArray[position] * (base ** exp)
	return result


# Task 1
sums = [0 for _ in range(len(data[0]))]
for line in data:
	for i in range(len(line)):
		sums[i] += int(line[i])

gammaBin, epsilonBin = [], []
for s in sums:
	if s < len(data) // 2:
		gammaBin.append(0)
		epsilonBin.append(1)
	if s > len(data) // 2:
		gammaBin.append(1)
		epsilonBin.append(0)

gamma, epsilon = binaryToDecimal(gammaBin), binaryToDecimal(epsilonBin)
print(gamma, epsilon)
print(gamma * epsilon)


# Task 2


def findRating(currentData, pos=0, least=False):
	if len(currentData) == 1:
		return [int(element) for element in currentData[0]]
	oneRows, zeroRows = [], []
	for binaryString in currentData:
		bit = int(binaryString[pos])
		if bit == 0:
			zeroRows.append(binaryString)
		if bit == 1:
			oneRows.append(binaryString)
	if least:
		newData = zeroRows if len(zeroRows) <= len(oneRows) else oneRows
	else:
		newData = oneRows if len(oneRows) >= len(zeroRows) else zeroRows
	return findRating(newData, pos + 1, least)


oxygenGenerator = binaryToDecimal(findRating(data.copy()))
co2Scrubber = binaryToDecimal(findRating(data.copy(), least=True))
print(oxygenGenerator, co2Scrubber)
print(oxygenGenerator * co2Scrubber)
