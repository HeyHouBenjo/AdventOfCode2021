import numpy as np


class Board:

	def __init__(self, numbers):
		self.values = np.reshape(numbers, (5, 5))
		self.marked = np.zeros((5, 5))

	def markNumber(self, num):
		self.marked[self.values == num] = 1

	def hasWon(self):
		byColumn = np.max(np.min(self.marked, axis=0))
		byRow = np.max(np.min(self.marked, axis=1))
		return byRow or byColumn

	def score(self):
		return self.values[self.marked == 0].sum()

	def __str__(self):
		return str(self.marked)


with open("input", "r") as file:
	numbersToCall = [int(strNum) for strNum in file.readline().split(",")]
	allBoardNumbers = [int(strNum) for strNum in file.read().split()]

boards = [Board(allBoardNumbers[i:i + 25]) for i in range(0, len(allBoardNumbers), 25)]

startLen = len(boards)
for number in numbersToCall:
	for board in boards[:]:
		board.markNumber(number)
		if board.hasWon():
			if len(boards) == startLen:
				finalScore = board.score() * number
				print(f"First score: {finalScore}")
			if len(boards) == 1:
				finalScore = board.score() * number
				print(f"Last score: {finalScore}")
			boards.remove(board)
	if len(boards) == 0:
		break
