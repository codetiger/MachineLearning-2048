import random
from copy import copy, deepcopy
from datetime import datetime
import numpy as np

class GameLogic:
	_gridSize = 4
	_gridMatrix = []
	_score = 0
	_render = False
	_normalize = False
	_bestScore = 0
	_invalidMoveCounter = 0

	def __init__(self, size = 4, random_seed = datetime.now()):
		self._gridSize = size
		self.reset(random_seed=random_seed)

	def reset(self, random_seed=datetime.now()):
		self._score = 0
		self._invalidMoveCounter = 0
		random.seed(datetime.now())

		self._fillEmptyGrid()
		self._addNewNumber()
		self._addNewNumber()

		return self._getState()

	def step(self, action):
		dir = action + 1

		gridCopy = [row[:] for row in self._gridMatrix]
		moveScore = 0

		for i in range(dir):
			self._gridMatrix = self._rotate(self._gridMatrix)

		for i in range(self._gridSize):
			temp = []
			for j in self._gridMatrix[i]:
				if j != 0:
				    temp.append(j)

			temp += [0] * self._gridMatrix[i].count(0)
			for j in range(len(temp) - 1):
				if temp[j] == temp[j + 1] and temp[j] != 0 and temp[j + 1] != 0:
					temp[j] = temp[j] + 1
					moveScore = 2**temp[j]
					temp[j + 1] = 0

			self._gridMatrix[i] = []
			for j in temp:
				if j != 0:
					self._gridMatrix[i].append(j)

			self._gridMatrix[i] += [0] * temp.count(0)

		for i in range(4 - dir):
			self._gridMatrix = self._rotate(self._gridMatrix)

		self._score += moveScore
		if self._bestScore < self._score:
			self._bestScore = self._score

		if self._gridMatrix == gridCopy:
			self._invalidMoveCounter += 1
		else:
			self._invalidMoveCounter = 0

		if self._invalidMoveCounter > 0:
			moveScore = self._invalidMoveCounter * -1

		self._addNewNumber()

		done = self._checkGameOver()

		if self._render:
			print("Dir: " + str(dir))
			self._printGrid()

		if done:
			moveScore = 0

		if self._normalize:
			if moveScore > 0:
				moveScore = np.log2(moveScore)

		return self._getState(), moveScore, done, {}

	def _fillEmptyGrid(self):
		self._gridMatrix = [[0 for col in range(self._gridSize)] for row in range(self._gridSize)]

	def _addNewNumber(self):
		count = 0
		for i in range(self._gridSize):
			count += self._gridMatrix[i].count(0)

		if count < 1: return False

		num = random.randint(1, 10)
		if num > 2: num = 1
		else: num = 2

		x = random.randint(0, self._gridSize-1)
		y = random.randint(0, self._gridSize-1)

		while self._gridMatrix[x][y]:
			x = random.randint(0, self._gridSize-1)
			y = random.randint(0, self._gridSize-1)

		self._gridMatrix[x][y] = num
		return True

	def _rotate(self, grid):
		return list(map(list, zip(*grid[::-1])))

	def _printGrid(self):
		print("\n")
		for i in range(self._gridSize):
			for j in range(self._gridSize):
				num = 0
				if self._gridMatrix[i][j]:
					num = 2**self._gridMatrix[i][j]
				print('{:4}'.format(num), end='')
			print("\n")
		print("\nScore:" + str(self._score))

	def _checkGameOver(self):
		def inner(b):
			for row in b:
				for x, y in zip(row[:-1], row[1:]):
					if x == y or x == 0 or y == 0:
						return True
			return False
		return not inner(self._gridMatrix) and not inner(zip(*self._gridMatrix))

	def _getMaxNumber(self):
		return max(map(max, self._gridMatrix))


	def _getState(self):
		maxNumber = 1.0
		if self._normalize:
			maxNumber = self._getMaxNumber()

		flatMat = [j/maxNumber for i in self._gridMatrix for j in i]
		return tuple(flatMat)