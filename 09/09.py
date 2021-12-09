import numpy as np

with open("input") as file:
	rows = file.read().splitlines()
	numbers = np.array([[int(num) for num in row] for row in rows])


def shift2D(arr, amount, vert=False, d=0):
	shifted = np.empty_like(arr)
	if vert:
		if amount > 0:
			shifted[:amount] = d
			shifted[amount:] = arr[:-amount]
		else:
			shifted[amount:] = d
			shifted[:amount] = arr[-amount:]
	else:
		if amount > 0:
			shifted[:, :amount] = d
			shifted[:, amount:] = arr[:, :-amount]
		else:
			shifted[:, amount:] = d
			shifted[:, :amount] = arr[:, -amount:]
	return shifted


def getLowPointsMask():
	m = np.max(numbers) + 1
	shR = shift2D(numbers, 1, d=m)
	shL = shift2D(numbers, -1, d=m)
	shU = shift2D(numbers, -1, True, d=m)
	shD = shift2D(numbers, 1, True, d=m)
	mask = (numbers < shR) & (numbers < shL) & (numbers < shU) & (numbers < shD)
	return mask


def solve1():
	lowPoints = numbers[getLowPointsMask()]
	return np.sum(lowPoints + 1)


def solve2():
	m = -1
	shR = shift2D(numbers, 1, d=m)
	shL = shift2D(numbers, -1, d=m)
	shU = shift2D(numbers, -1, True, d=m)
	shD = shift2D(numbers, 1, True, d=m)
	leftGreater = numbers < shR
	rightGreater = numbers < shL
	upGreater = numbers < shD
	downGreater = numbers < shU

	def search(fromX, fromY):
		if (fromX, fromY) in visited or numbers[fromY][fromX] == 9:
			return
		visited.add((fromX, fromY))
		if leftGreater[fromY, fromX]:
			search(fromX - 1, fromY)
		if rightGreater[fromY, fromX]:
			search(fromX + 1, fromY)
		if downGreater[fromY, fromX]:
			search(fromX, fromY + 1)
		if upGreater[fromY, fromX]:
			search(fromX, fromY - 1)

	sizes = [0, 0, 0]
	for y, x in np.transpose(np.where(getLowPointsMask())):
		visited = set()
		search(x, y)
		n = len(visited)
		if n > min(sizes):
			sizes.remove(min(sizes))
			sizes.append(n)

	return sizes[0] * sizes[1] * sizes[2]


print(solve1())
print(solve2())
