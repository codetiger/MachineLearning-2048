import numpy as np
import gym
import random
import time

from keras.models import Sequential, Model, Input
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy, BoltzmannQPolicy, LinearAnnealedPolicy
from rl.memory import SequentialMemory

from gamelogic import *
from datetime import datetime
import numpy, time
from evostra import EvolutionStrategy
import pylab

ENV_NAME = "2048"


class Agent:
	AGENT_HISTORY_LENGTH = 1
	POPULATION_SIZE = 20
	EPS_AVG = 1
	SIGMA = 0.1
	LEARNING_RATE = 0.01
	INITIAL_EXPLORATION = 1.0
	FINAL_EXPLORATION = 0.01
	EXPLORATION_DEC_STEPS = 50000

	plotScores = []
	plotEpisodes = []
	plotMaxTiles = []
	plotEpiCounter = 0

	GRID_SIZE = 3

	action_space = [0, 1, 2, 3]

	def __init__(self):
		random.seed(int(time.time()))
		np.random.seed(int(time.time()))

		window_length = 1
		nb_hidden = 256
		nb_actions = 4

		self.env = GameLogic(size = self.GRID_SIZE)

		input_layer = Input(shape=(1, self.GRID_SIZE * self.GRID_SIZE))

		layer = Dense(8)(input_layer)
		output_layer = Dense(3)(layer)
		
		self.model = Model(input_layer, output_layer)
		self.model.compile(Adam(), 'mse')

		# self.model = Sequential()
		# self.model.add(Flatten(input_shape=(window_length, self.GRID_SIZE * self.GRID_SIZE)))
		# self.model.add(Dense(nb_hidden))
		# self.model.add(Activation('relu'))
		# self.model.add(Dense(nb_hidden))
		# self.model.add(Activation('relu'))
		# self.model.add(Dense(nb_actions, activation='linear'))
		# print(self.model.summary())

		self.es = EvolutionStrategy(self.model.get_weights(), self.get_reward, self.POPULATION_SIZE, self.SIGMA, self.LEARNING_RATE)
		self.exploration = self.INITIAL_EXPLORATION

	def get_predicted_action(self, sequence):
		prediction = self.model.predict(np.array(sequence))
		return prediction

	def load(self, filename='weights.pkl'):
		self.model.load_weights(filename)
		self.es.weights = self.model.get_weights()

	def save(self, filename='weights.pkl'):
		self.model.save_weights(filename, overwrite=True)

	def play(self, episodes, render=True):
		self.model.set_weights(self.es.weights)
		for episode in range(episodes):
			total_reward = 0
			observation = self.env.reset()
			done = False
			while not done:
				action = self.model.predict(np.array(observation))
				observation, reward, done, _ = self.env.step(action)
				total_reward += reward
		print("total reward: " + str(total_reward))

	def train(self, iterations):
		self.es.run(iterations, print_step=1)

	def get_reward(self, weights):
		total_reward = 0.0
		self.model.set_weights(weights)

		for episode in range(self.EPS_AVG):
			observation = self.env.reset()
			observation = np.reshape(observation, [1, self.GRID_SIZE * self.GRID_SIZE])
			done = False
			while not done:
				self.exploration = max(self.FINAL_EXPLORATION, self.exploration - self.INITIAL_EXPLORATION/self.EXPLORATION_DEC_STEPS)
				if random.random() < self.exploration:
					action = random.randint(0, 3)
				else:
					action = np.argmax(self.model.predict(np.array([observation]))[0])

				observation, reward, done, _ = self.env.step(action)
				observation = np.reshape(observation, [1, self.GRID_SIZE * self.GRID_SIZE])
				total_reward += reward

		self.plotEpiCounter += 1
		self.plotEpisodes.append(self.plotEpiCounter)
		self.plotScores.append(self.env._score)
		self.plotMaxTiles.append(2**self.env._getMaxNumber())

		pylab.plot(self.plotEpisodes, self.plotScores, '-b', label='Score')
		pylab.plot(self.plotEpisodes, self.plotMaxTiles, '-r', label='Max Tile')
		pylab.savefig('evostra_{}_{}x.png'.format(ENV_NAME, self.GRID_SIZE))

		print("Game Score: {} Max Tile: {} Exploration: {}".format(self.env._score, 2**self.env._getMaxNumber(), self.exploration))
		return total_reward/self.EPS_AVG

agent = Agent()

try:
	agent.load()
except:
	pass

agent.train(10)
agent.save()

