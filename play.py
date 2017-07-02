from gamelogic import *
from ddqn import DQNAgent
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras import backend as K
import gym
import numpy as np

EPISODES = 1000

if __name__ == "__main__":
    gridSize = 2
    gameEnv = GameLogic(gridSize)

    state_size = gridSize * gridSize
    action_size = 4
    agent = DQNAgent(state_size, action_size)
    agent.load("2048.h5")
    done = False
    batch_size = 64
    bestScore = 0

    try:
        with open("bestscore.txt", "r") as file:
            data = file.read()
            if data:
                bestScore = int(data)
    except IOError:
        bestScore = 0


    for e in range(EPISODES):
        gameEnv.Reset()
        state = gameEnv.GetFlatGrid()
        state = np.reshape(state, [1, state_size])
        reward = gameEnv.GetScore()

        while True:
            action = agent.act(state)
            gameEnv.Move(action + 1)
            gameEnv.AddNewNumber()

            next_state = gameEnv.GetFlatGrid()
            next_state = np.reshape(next_state, [1, state_size])
            next_reward = gameEnv.GetScore() - reward
            done = gameEnv.CheckGameOver()

            # gameEnv.PrintGrid()

            agent.remember(state, action, reward, next_state, done)
            state = next_state
            reward = next_reward
            if done:
                agent.update_target_model()
                print("episode: {}/{}, score: {}, e: {:.2}".format(e, EPISODES, reward, agent.epsilon))
                break

        if len(agent.memory) > batch_size:
            agent.replay(batch_size)
        if e % 10 == 0:
            agent.save("2048.h5")
