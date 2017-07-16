import numpy as np
import gym

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy, BoltzmannQPolicy, LinearAnnealedPolicy
from rl.memory import SequentialMemory
from rl.callbacks import Callback

from gamelogic import *
from datetime import datetime
import numpy, time
import csv

ENV_NAME = "2048"

class LivePlotCallback(Callback):
	def __init__(self, env, filePath):
		self._env = env
		_csvFile = open(filePath, "w")
		self._csvWriter = csv.writer(_csvFile, delimiter=',')

	def on_episode_end(self, episode, logs):
		self._csvWriter.writerow((episode, self._env._score, 2**self._env._getMaxNumber()))


if __name__ == "__main__":
	# Get the environment and extract the number of actions.
	gridSize = 3

	random.seed(int(time.time()))
	np.random.seed(int(time.time()))

	env = GameLogic(size = gridSize)
	env._normalize = True
	# env._reset2RandomBoard = True
	env.reset()

	nb_actions = 4
	nb_steps = int(2e6)
	nb_steps_annealed = int(1.25e6)
	nb_steps_warmup = int(0.25e6)
	window_length = 1
	nb_hidden = 256
	memory_size = int(2e6)
	batch_size = 256
	delta_clip = 1.0
	train_interval = 100

	# Next, we build a very simple model regardless of the dueling architecture
	# if you enable dueling network in DQN , DQN will build a dueling network base on your model automatically
	# Also, you can build a dueling network by yourself and turn off the dueling network in DQN.

	model = Sequential()
	model.add(Flatten(input_shape=(window_length, gridSize * gridSize)))
	model.add(Dense(nb_hidden))
	model.add(Activation('relu'))
	model.add(Dense(nb_hidden))
	model.add(Activation('relu'))
	model.add(Dense(nb_actions, activation='linear'))
	print(model.summary())

	# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
	# even the metrics!
	memory = SequentialMemory(limit=memory_size, window_length=window_length)

	policy = EpsGreedyQPolicy(eps=.01)

	dqn = DQNAgent(model=model, nb_actions=nb_actions, test_policy=policy, policy=policy, memory=memory)
	
	dqn.compile(Adam(lr=.00025), metrics=['mae'])

	dqn.load_weights('dqn_{}_weights_{}x.h5f'.format(ENV_NAME, gridSize))

	cbs = [LivePlotCallback(env=env, filePath='dqn_{}_test_{}x.csv'.format(ENV_NAME, gridSize))]

	env._verbose = 1
	env.reset()
	# Finally, evaluate our algorithm for 5 episodes.
	dqn.test(env, nb_episodes=100, visualize=False, verbose=1, callbacks=cbs)
