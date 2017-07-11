import numpy as np
import gym

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy, BoltzmannQPolicy, LinearAnnealedPolicy
from rl.memory import SequentialMemory

from gamelogic import *
from datetime import datetime
import numpy, time

ENV_NAME = "2048"

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

	policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=1., value_min=.1, value_test=.05, nb_steps=10000)

	dqn = DQNAgent(model=model, nb_actions=nb_actions, policy=policy, memory=memory, nb_steps_warmup=5000, gamma=.99, target_model_update=10000, train_interval=4, delta_clip=1.)
	
	dqn.compile(Adam(lr=.00025), metrics=['mae'])

	try:
		dqn.load_weights('duel_dqn_{}_weights_{}x.h5f'.format(ENV_NAME, gridSize))
	except:
		pass
	# Okay, now it's time to learn something! We visualize the training here for show, but this
	# slows down training quite a lot. You can always safely abort the training prematurely using
	# Ctrl + C.
	dqn.fit(env, nb_steps=9999999, visualize=False, verbose=1)

	# After training is done, we save the final weights.
	dqn.save_weights('duel_dqn_{}_weights_{}x.h5f'.format(ENV_NAME, gridSize), overwrite=True)

	# env._render= True
	# env.reset()
	# # Finally, evaluate our algorithm for 5 episodes.
	# dqn.test(env, nb_episodes=5, visualize=False)
