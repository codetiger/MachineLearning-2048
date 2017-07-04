#!/usr/bin/env python3 

import random
from copy import copy, deepcopy
from datetime import datetime

class GameLogic:
	gridSize = 4
	gridMatrix = []
	score = 0

	def __init__(self, size):
		self.gridSize = size
		self.Reset()

	def Reset(self):
		random.seed(datetime.now())
		# random.seed(0)
		self.FillEmptyGrid()
		self.AddNewNumber()
		self.AddNewNumber()

	def FillEmptyGrid(self):
		self.score = 0
		self.gridMatrix = [[0 for col in range(self.gridSize)] for row in range(self.gridSize)]

	def AddNewNumber(self):
		count = 0
		for i in range(self.gridSize):
			count += self.gridMatrix[i].count(0)

		if count < 1: return False

		num = random.randint(1, 10)
		if num > 2: num = 1
		else: num = 2

		x = random.randint(0, self.gridSize-1)
		y = random.randint(0, self.gridSize-1)

		while self.gridMatrix[x][y]:
			x = random.randint(0, self.gridSize-1)
			y = random.randint(0, self.gridSize-1)

		self.gridMatrix[x][y] = num
		return True

	def rotate(self, grid):
		return list(map(list, zip(*grid[::-1])))

	def Move(self, dir):
		gridCopy = [row[:] for row in self.gridMatrix]
		moveScore = 0

		for i in range(dir):
			self.gridMatrix = self.rotate(self.gridMatrix)

		for i in range(self.gridSize):
			temp = []
			for j in self.gridMatrix[i]:
				if j != 0:
				    temp.append(j)

			temp += [0] * self.gridMatrix[i].count(0)
			for j in range(len(temp) - 1):
				if temp[j] == temp[j + 1] and temp[j] != 0 and temp[j + 1] != 0:
					temp[j] = temp[j] + 1
					moveScore = 2**temp[j]
					temp[j + 1] = 0

			self.gridMatrix[i] = []
			for j in temp:
				if j != 0:
					self.gridMatrix[i].append(j)

			self.gridMatrix[i] += [0] * temp.count(0)

		for i in range(4 - dir):
			self.gridMatrix = self.rotate(self.gridMatrix)

		self.score += moveScore
		return (moveScore, self.gridMatrix != gridCopy)

	def PrintGrid(self):
		print("\n")
		for i in range(self.gridSize):
			for j in range(self.gridSize):
				num = 0
				if self.gridMatrix[i][j]:
					num = 2**self.gridMatrix[i][j]
				print('{:4}'.format(num), end='')
			print("\n")
		print("\nScore:" + str(self.score))

	def CheckGameOver(self):
		def inner(b):
			for row in b:
				for x, y in zip(row[:-1], row[1:]):
					if x == y or x == 0 or y == 0:
						return True
			return False
		return not inner(self.gridMatrix) and not inner(zip(*self.gridMatrix))

	def GetScore(self):
		return self.score

	def GetMaxNumber(self):
		return max(map(max, self.gridMatrix))

	def GetValueIn(self, i, j):
		return self.gridMatrix[i][j]

	def GetMatrix(self):
		return self.gridMatrix

	def GetFlatGrid(self):
		return [j for i in self.gridMatrix for j in i]
		# maxNumber = self.GetMaxNumber()
		# return [j/maxNumber for i in self.gridMatrix for j in i]
