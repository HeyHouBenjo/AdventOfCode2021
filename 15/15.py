import math

with open("input") as file:
	rawWeights = [[int(num) for num in line] for line in file.read().splitlines()]

Node = tuple[int, int]


# this is a performance killer -> O(n)
def popMinNode(openList: dict[Node, int]) -> Node:
	node, _ = min(openList.items(), key=lambda elem: elem[1])
	openList.pop(node)
	return node


def getNeighbours(node: Node, size):
	x, y = node
	return set(filter(
		lambda n: 0 <= n[0] < size and 0 <= n[1] < size, {
			(x + 1, y),
			(x - 1, y),
			(x, y + 1),
			(x, y - 1)
		}
	))


# Dijkstra without priority queue -> super slow...
def findPath(weights):
	size = len(weights)
	target = (size, size)
	openList, closedList = {(0, 0): 0}, set()
	dists = {(x, y): math.inf for x in range(size) for y in range(size)}
	pres = {(x, y): None for x in range(size) for y in range(size)}
	dists[(0, 0)] = 0
	while len(openList) > 0:
		currentNode = popMinNode(openList)
		if currentNode == target:
			# path found
			break
		closedList.add(currentNode)
		for successor in getNeighbours(currentNode, size).difference(closedList):
			x, y = successor
			d = dists[currentNode] + weights[y][x]
			if successor in openList.keys() and d >= dists[successor]:
				continue
			pres[successor] = currentNode
			dists[successor] = d
			openList[successor] = d

	node = (size - 1, size - 1)
	risk = 0
	while node != (0, 0):
		x, y = node
		risk += weights[y][x]
		node = pres[node]
	print(risk)


def expandWeights(weights):
	size = len(weights)
	parts = [[[val for val in row] for row in weights]]
	for i in range(8):
		part = parts[i]
		added = [[val + 1 if val < 9 else 1 for val in row] for row in part]
		parts.append(added)

	newWeights = []
	for y in range(5):
		row = parts[y]
		for x in range(4):
			addRight = parts[y + x + 1]
			for i in range(size):
				row[i] += addRight[i]
		newWeights.extend(row)

	return newWeights


findPath(rawWeights)
findPath(expandWeights(rawWeights))
