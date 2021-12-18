from __future__ import annotations
import copy
import json
from typing import Union
from itertools import combinations


class Regular:

	def __init__(self, value):
		self.value = value
		self.parent: Pair = None

	def split(self):
		newLeft = Regular(self.value // 2)
		newRight = Regular(self.value // 2 + self.value % 2)
		newPair = Pair(newLeft, newRight)
		newPair.parent = self.parent
		if self == self.parent.left:
			self.parent.left = newPair
		if self == self.parent.right:
			self.parent.right = newPair

	def __repr__(self):
		return f"{self.value}"


class Pair:

	def __init__(self, left: Union[Pair, Regular], right: Union[Pair, Regular]):
		self.left = left
		self.right = right
		left.parent = self
		right.parent = self
		self.parent: Pair = None

	@staticmethod
	def neutral() -> Pair:
		pair = Pair.parse([0, 0])
		pair.left = None
		return pair

	@staticmethod
	def parse(content) -> Union[Pair, int]:
		if isinstance(content, int):
			return Regular(content)
		left, right = content
		return Pair(Pair.parse(left), Pair.parse(right))

	def __add__(self, other) -> Pair:
		if self.left is None:
			return other
		pair = Pair(copy.deepcopy(self), copy.deepcopy(other))
		pair.reduce()
		return pair

	def getExplodePair(self, dim=0) -> Pair:
		if dim == 4:
			return self

		def checkSide(side):
			if isinstance(side, Pair):
				pair = side.getExplodePair(dim + 1)
				if isinstance(pair, Pair):
					return pair
		if explode := checkSide(self.left):
			return explode
		if explode := checkSide(self.right):
			return explode

	def getSplitRegular(self) -> Regular:
		leftIsRegular = isinstance(self.left, Regular)
		rightIsRegular = isinstance(self.right, Regular)
		if leftIsRegular:
			if self.left.value >= 10:
				return self.left
		elif left := self.left.getSplitRegular():
			return left
		if rightIsRegular:
			if self.right.value >= 10:
				return self.right
		elif right := self.right.getSplitRegular():
			return right
		return None

	def findRegularLeft(self) -> Regular:
		if self.parent is None:
			return None
		if self == self.parent.right:
			if isinstance(self.parent.left, Regular):
				return self.parent.left
			return self.parent.left.findLastRegular()
		return self.parent.findRegularLeft()

	def findRegularRight(self) -> Regular:
		if self.parent is None:
			return None
		if self == self.parent.left:
			if isinstance(self.parent.right, Regular):
				return self.parent.right
			return self.parent.right.findFirstRegular()
		return self.parent.findRegularRight()

	def findFirstRegular(self) -> Regular:
		if isinstance(self.left, Regular):
			return self.left
		return self.left.findFirstRegular()

	def findLastRegular(self) -> Regular:
		if isinstance(self.right, Regular):
			return self.right
		return self.right.findLastRegular()

	def explode(self):
		regularLeft = self.findRegularLeft()
		regularRight = self.findRegularRight()
		if regularLeft:
			regularLeft.value += self.left.value
		if regularRight:
			regularRight.value += self.right.value
		zero = Regular(0)
		zero.parent = self.parent
		if self == self.parent.left:
			self.parent.left = zero
		if self == self.parent.right:
			self.parent.right = zero

	def reduce(self):
		while (toExplode := self.getExplodePair()) or (toSplit := self.getSplitRegular()):
			if toExplode:
				toExplode.explode()
				continue
			toSplit.split()

	def magnitude(self):
		left = self.left.value if isinstance(self.left, Regular) else self.left.magnitude()
		right = self.right.value if isinstance(self.right, Regular) else self.right.magnitude()
		return left * 3 + right * 2

	def __repr__(self):
		return f"({self.left}, {self.right})"


def parseNumbers(fileName: str) -> list[Pair]:
	with open(fileName) as file:
		lines = file.read().splitlines()
	return [Pair.parse(json.loads(line)) for line in lines]


allNumbers = parseNumbers("input")
print(sum(allNumbers, Pair.neutral()).magnitude())
print(max([max((a + b).magnitude(), (b + a).magnitude()) for a, b in combinations(allNumbers, 2)]))
