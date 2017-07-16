import random
from datetime import datetime
import numpy as np
import time

class GameLogic:
	_gridSize = 4
	_gridMatrix = []
	_score = 0
	_verbose = 0
	_normalize = False
	_bestScore = 0
	_invalidMoveCounter = 0
	_reset2RandomBoard = False

	def __init__(self, size = 4):
		self._gridSize = size
		self.reset()

	def reset(self):
		self._score = 0
		self._invalidMoveCounter = 0

		if self._reset2RandomBoard:
			self._generateRandomBoard()
		else:
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
			self._invalidMoveCounter = self._invalidMoveCounter + 1
			moveScore = self._invalidMoveCounter * -1
		else:
			self._invalidMoveCounter = 0
			self._addNewNumber()

		done = self._checkGameOver()

		if self._verbose >= 2:
			self._printGrid()
		
		if self._verbose >= 1 and done:
			self._printGrid()
			print("Score: " + str(self._score) + " MaxTile: " + str(2**self._getMaxNumber()))

		if done:
			moveScore = -100

		if moveScore > 0 and self._checkOptimInAllDir(self._gridMatrix):
			moveScore = 10

		state = self._getState()	

		# if self._normalize:
		# 	if moveScore > 0:
		# 		moveScore = np.log2(moveScore)

		return state, moveScore, done, {}

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
		self._printMatrix(self._gridMatrix)

	def _printMatrix(self, matrix):
		for i in range(self._gridSize):
			for j in range(self._gridSize):
				num = 0
				if matrix[i][j]:
					num = 2**matrix[i][j]
				print('{:4}'.format(num), end='')
			print("")

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

	def _checkOptimInAllDir(self, matrix):
		gridCopy = [row[:] for row in matrix]

		for i in range(4):  #Check through all directions
			gridCopy = self._rotate(gridCopy)
			for j in range(2):  #Check through both mirrors
				gridCopy = gridCopy[::-1]
				if self._checkOptimInMatrix(gridCopy):
					return True

		return False

	def _checkOptimInMatrix(self, matrix):
		reverseRow = True
		newFlatMat = [] # builds a 1d list in zipzag order
		for row in matrix:
			reverseRow = not reverseRow
			newRow = row
			if reverseRow:
				newRow = reversed(row)
			for val in newRow:
				newFlatMat = newFlatMat + [val]

		newFlatMat = [x for x in newFlatMat if x != 0] # removes 0s from the list

		if all(earlier >= later for earlier, later in zip(newFlatMat, newFlatMat[1:])):
			return True
		elif all(earlier <= later for earlier, later in zip(newFlatMat, newFlatMat[1:])):
			return True
		else:
			return False

	def _generateRandomBoard(self):
		self._fillEmptyGrid()
		numRandTiles = random.randint(2, self._gridSize*self._gridSize)

		for n in range(numRandTiles):
			x = random.randint(0, self._gridSize-1)
			y = random.randint(0, self._gridSize-1)
			self._gridMatrix[x][y] = random.randint(0, self._gridSize - 1)