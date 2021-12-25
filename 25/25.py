import sys

import numpy as np
from PyQt5.QtCore import QTimer, QSize
from PyQt5.QtGui import QPaintEvent, QPixmap, QImage, QPainter, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QLabel


def readGrid(fileName):
	with open(fileName) as file:
		lines = file.read().splitlines()
	grid = [list(line) for line in lines]
	return np.array(grid)


def step(herdName: str, grid: np.ndarray) -> int:
	# all places that want to move
	toMove = grid == herdName

	# complete grid shifted back one index
	gridShiftedBack = np.roll(grid, -1, 1 if herdName == ">" else 0)

	# can only move onto a dot
	toMove[gridShiftedBack != '.'] = False

	# moving objects leave a dot
	grid[toMove] = '.'

	# move objects by shifting forward on correct axis
	toMoveShiftedForward = np.roll(toMove, 1, 1 if herdName == ">" else 0)

	# set new values
	grid[toMoveShiftedForward] = herdName

	return len(grid[toMove])


def findPlace():
	grid = readGrid("input")
	count = 1
	while step('>', grid) + step('v', grid) > 0:
		count += 1
	print(count)


class AnimatorWindow(QWidget):

	def __init__(self):
		super().__init__()
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.step)
		self.timer.setInterval(16)
		self.timer.start()

		self.grid = readGrid("input")
		h, w = self.grid.shape
		self.w = w * 5
		self.h = h * 5
		self.resize(self.w, self.h)
		self.label = QLabel(self)
		self.label.resize(self.w, self.h)

	def getImage(self):
		h, w = self.grid.shape
		colorArray = np.zeros((w, h, 3), dtype=np.uint8)

		# something is still wrong here ):
		a = np.argwhere(self.grid == ">").T
		b = np.argwhere(self.grid == "v").T
		colorArray[a[1], a[0]] = [255, 0, 0]
		colorArray[b[1], b[0]] = [0, 255, 0]

		image = QImage(colorArray.data, w, h, 3 * w, QImage.Format_RGB888)
		return image.scaled(self.w, self.h)

	def step(self):
		step(">", self.grid)
		step("v", self.grid)

		self.label.setPixmap(QPixmap.fromImage(self.getImage()))


if __name__ == "__main__":
	app = QApplication(sys.argv)

	window = AnimatorWindow()
	window.show()

	app.exec()
