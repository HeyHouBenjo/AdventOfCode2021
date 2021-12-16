def multiply(arr: list[int]) -> int:
	val = 1
	for elem in arr:
		val *= elem
	return val


hexToBinMap = {
	"0": "0000",
	"1": "0001",
	"2": "0010",
	"3": "0011",
	"4": "0100",
	"5": "0101",
	"6": "0110",
	"7": "0111",
	"8": "1000",
	"9": "1001",
	"A": "1010",
	"B": "1011",
	"C": "1100",
	"D": "1101",
	"E": "1110",
	"F": "1111"
}
typeIdToOperationMap = {
	0: lambda values: sum(values),
	1: lambda values: multiply(values),
	2: lambda values: min(values),
	3: lambda values: max(values),
	5: lambda values: 1 if values[0] > values[1] else 0,
	6: lambda values: 1 if values[0] < values[1] else 0,
	7: lambda values: 1 if values[0] == values[1] else 0
}


def readInput(name):
	with open(name) as file:
		binary = ""
		for char in file.read().removesuffix("\n"):
			binary += hexToBinMap[char]
	return binary


class Packet:

	def __init__(self, version: int):
		self.version = version
		self.bitLength = 6

	def getVersionSum(self) -> int:
		return self.version

	def calculate(self) -> int:
		pass


class LiteralValue(Packet):

	def __init__(self, version: int, content: str):
		super().__init__(version)
		self.value = None
		self.parse(content)

	def parse(self, content: str):
		groups = []
		label = "1"
		while label == "1":
			i = len(groups) * 5
			label = content[i]
			groups.append(content[i+1:i+5])
		self.value = int("".join(groups), 2)
		self.bitLength += len(groups) * 5

	def calculate(self) -> int:
		return self.value


class Operator(Packet):

	def __init__(self, version: int, content: str, typeId: int):
		super().__init__(version)
		self.typeId = typeId
		self.subPackets: list[Packet] = []
		self.parse(content)

	def getVersionSum(self):
		return super().getVersionSum() + sum([p.getVersionSum() for p in self.subPackets])

	def parse(self, content: str):
		lengthTypeId = int(content[0])
		self.bitLength += 1
		if lengthTypeId == 0:
			self.bitLength += 15
			subPacketBitLength = int(content[1:16], 2)
			self.parseSubPackets(content[16:16 + subPacketBitLength])
		if lengthTypeId == 1:
			self.bitLength += 11
			subPacketCount = int(content[1:12], 2)
			self.parseSubPackets(content[12:], subPacketCount)

	def parseSubPackets(self, content: str, subPacketCount: int = None):
		pos = 0
		while pos < len(content) and (subPacketCount is None or len(self.subPackets) < subPacketCount):
			packet = parsePacket(content[pos:])
			pos += packet.bitLength
			self.subPackets.append(packet)
		self.bitLength += pos

	def calculate(self) -> int:
		subResults = [p.calculate() for p in self.subPackets]
		return typeIdToOperationMap[self.typeId](subResults)


def parsePacket(binary: str):
	version = int(binary[:3], 2)
	typeId = int(binary[3:6], 2)
	if typeId == 4:
		return LiteralValue(version, binary[6:])
	else:
		return Operator(version, binary[6:], typeId)


mainPacket = parsePacket(readInput("input"))
print(mainPacket.getVersionSum())
print(mainPacket.calculate())
