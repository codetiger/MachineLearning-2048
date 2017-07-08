import numpy as np
import gym

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy, BoltzmannQPolicy
from rl.memory import SequentialMemory

from gamelogic import *
from datetime import datetime

ENV_NAME = "2048"

if __name__ == "__main__":
	# Get the environment and extract the number of actions.
	gridSize = 4

	env = GameLogic(size = gridSize)
	env._normalize = True
	env.reset(random_seed=datetime.now())

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
	policy = BoltzmannQPolicy()

	dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=10,
               enable_dueling_network=True, dueling_type='avg', target_model_update=1e-2, policy=policy)
	
	dqn.compile(Adam(lr=1e-3), metrics=['mae'])

	# Okay, now it's time to learn something! We visualize the training here for show, but this
	# slows down training quite a lot. You can always safely abort the training prematurely using
	# Ctrl + C.
	dqn.fit(env, nb_steps=999999, visualize=False, verbose=1)

	# After training is done, we save the final weights.
	dqn.save_weights('duel_dqn_{}_weights.h5f'.format(ENV_NAME), overwrite=True)

	env._render= True
	env.reset(random_seed=datetime.now())
	# Finally, evaluate our algorithm for 5 episodes.
	dqn.test(env, nb_episodes=5, visualize=False)
