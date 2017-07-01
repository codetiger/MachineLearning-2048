from gamelogic import *
import sys,tty,termios
import random
from tkinter import *
from tkinter import messagebox

KEY_UP_ALT = "\'\\uf700\'"
KEY_DOWN_ALT = "\'\\uf701\'"
KEY_LEFT_ALT = "\'\\uf702\'"
KEY_RIGHT_ALT = "\'\\uf703\'"

KEY_UP = "'w'"
KEY_DOWN = "'s'"
KEY_LEFT = "'a'"
KEY_RIGHT = "'d'"

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {   2:"#eee4da", 4:"#ede0c8", 8:"#f2b179", 16:"#f59563", \
                            32:"#f67c5f", 64:"#f65e3b", 128:"#edcf72", 256:"#edcc61", \
                            512:"#edc850", 1024:"#edc53f", 2048:"#edc22e" }
CELL_COLOR_DICT = { 2:"#776e65", 4:"#776e65", 8:"#f9f6f2", 16:"#f9f6f2", \
                    32:"#f9f6f2", 64:"#f9f6f2", 128:"#f9f6f2", 256:"#f9f6f2", \
                    512:"#f9f6f2", 1024:"#f9f6f2", 2048:"#f9f6f2" }
FONT = ("Verdana", 40, "bold")

SIZE = 500
GRID_PADDING = 10

class GameManager(Frame):
	bestScore = 0
	allTimeBestScore = 0
	episodes = 1
	highestNumber = 0
	game = None
	grid_cells = []
	gridSize = 2

	def __init__(self):
		Frame.__init__(self)

		self.grid()
		self.game = GameLogic(self.gridSize)
		self.bestScore = 0
		self.allTimeBestScore = 0
		self.episodes = 1
		self.highestNumber = 0

		self.master.title('2048')
		self.master.bind("<Key>", self.key_down)
		self.master.resizable(width=False, height=False)
		self.commands = {   KEY_UP: 3, KEY_DOWN: 1, KEY_LEFT: 4, KEY_RIGHT: 2,
							KEY_UP_ALT: 3, KEY_DOWN_ALT: 1, KEY_LEFT_ALT: 4, KEY_RIGHT_ALT: 2 }
		self.init_grid()
		self.update_grid_cells()
		self.mainloop()

	def init_grid(self):
		background = Frame(self, bg="#92877d", width=SIZE, height=SIZE)
		background.grid()

		for i in range(self.gridSize):
		    grid_row = []
		    for j in range(self.gridSize):
		        cell = Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE/self.gridSize, height=SIZE/self.gridSize)
		        cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
		        # font = Font(size=FONT_SIZE, family=FONT_FAMILY, weight=FONT_WEIGHT)
		        t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4, height=2)
		        t.grid()
		        grid_row.append(t)

		    self.grid_cells.append(grid_row)

	def update_grid_cells(self):
	    for i in range(self.gridSize):
	        for j in range(self.gridSize):
	            new_number = self.game.GetValueIn(i, j)
	            if new_number == 0:
	                self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
	            else:
	                self.grid_cells[i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT[new_number], fg=CELL_COLOR_DICT[new_number])
	    self.update_idletasks()

	def readBestScore(self):
		try:
			with open("bestscore.txt", "r") as file:
				data = file.read()
				if data:
					self.allTimeBestScore = int(data)
		except IOError:
			self.allTimeBestScore = 0

	def key_down(self, event):
		dir = repr(event.char)
		if dir in self.commands:
			if self.game.Move(self.commands[dir]):
				self.game.AddNewNumber()
		self.update_grid_cells()

		if self.game.CheckGameOver():
			file = open("bestscore.txt", "w")
			file.write(str(self.allTimeBestScore))
			messagebox.showinfo("Game Over", "You lost the game! Try again...")
			print("\nBest Score: " + str(self.bestScore) + "\tAllTimeBest: " + str(self.allTimeBestScore) + "\tHigesh Number: " + str(self.highestNumber))
			self.master.destroy()

	def getRandomAction(self):
		if random.randint(0, 10) > 8:
			dir = random.randint(3, 4)
		else:
			dir = random.randint(1, 2)
		return dir

	def gameMain(self):
		print("\nWelcome to the 2048!")

		for x in range(0, self.episodes):
			self.game.Reset()

			while not self.game.CheckGameOver():
				dir = self.getHumanAction()
				# dir = getRandomAction()
				if dir == 0:
					break

				if self.game.Move(dir):
					self.game.AddNewNumber()

				self.game.PrintGrid()

			if self.allTimeBestScore < self.game.score:
				self.allTimeBestScore = self.game.score

			if self.bestScore < self.game.score:
				self.bestScore = self.game.score

			if self.highestNumber < self.game.maxNumber:
				self.highestNumber = self.game.maxNumber

		file = open("bestscore.txt", "w")
		file.write(str(self.allTimeBestScore))

		print("\nBest Score: " + str(bestScore) + "\tAllTimeBest: " + str(allTimeBestScore) + "\tHigesh Number: " + str(highestNumber))

gameMan = GameManager()
