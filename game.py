from gamelogic import *
import sys,tty,termios
import random 

def getch():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(3)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

def getHumanAction():
	k = getch()
	dir = 0
	if k=='\x1b[A':
		dir = 3
	elif k=='\x1b[B':
		dir = 1
	elif k=='\x1b[C':
		dir = 2
	elif k=='\x1b[D':
		dir = 4
	return dir

def getRandomAction():
	if random.randint(0, 10) > 8:
		dir = random.randint(3, 4)
	else:
		dir = random.randint(1, 2)
	return dir

print "\nWelcome to the 2048!"
bestScore = 0
allTimeBestScore = 0
episodes = 1
highestNumber = 0

game = GameLogic(4)

try:
	with open("bestscore.txt", "r") as file:
		data = file.read()
		if data:
			allTimeBestScore = int(data)
except IOError:
	allTimeBestScore = 0

for x in xrange(0, episodes):
	game.Reset()

	while not game.CheckGameOver():
		dir = getHumanAction()
		# dir = getRandomAction()
		if dir == 0:
			break	

		if game.Move(dir):
			game.AddNewNumber()

		game.PrintGrid()

	if allTimeBestScore < game.score:
		allTimeBestScore = game.score

	if bestScore < game.score:
		bestScore = game.score

	if highestNumber < game.maxNumber:
		highestNumber = game.maxNumber

file = open("bestscore.txt", "w")
file.write(str(allTimeBestScore))

print "\nBest Score: " + str(bestScore) + "\tAllTimeBest: " + str(allTimeBestScore) + "\tHigesh Number: " + str(highestNumber)