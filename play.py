from gamelogic import *
from ddqn import DoubleDQNAgent
# from dqn import DQNAgent
# from ql import QLearningAgent
# from rl import REINFORCEAgent

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras import backend as K
import gym
import numpy as np
import pylab

EPISODES = 1000

def getPeaks(arr):
    peaks = []
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if checkPeak(arr, i, j):
                peaks.append((i, j))
    return peaks

def checkPeak(arr, i, j):
    if arr[i][j] == 0:
        return False

    cells = [(i+1, j+0), (i+0, j+1), (i-1, j+0), (i+0, j-1)]
    greaterCells = 0
    for n in range(len(cells)):
        (x, y) = cells[n]
        if x >= 0 and x < len(arr) and y >= 0 and y < len(arr[x]) and arr[x][y] >= arr[i][j]:
            greaterCells += 1

    return greaterCells == 0

if __name__ == "__main__":
    gridSize = 4
    gameEnv = GameLogic(gridSize)

    state_size = gridSize * gridSize
    action_size = 4

    agent = DoubleDQNAgent(state_size, action_size)

    # agent = DoubleDQNAgent(state_size, action_size)

    try:
        agent.model.load_weights("2048_"+str(gridSize)+".h5")
    except IOError:
        pass

    done = False
    scores, episodes = [], []

    for e in range(EPISODES):
        gameEnv.Reset()
        state = gameEnv.GetFlatGrid()
        state = np.reshape(state, [1, state_size])
        reward = 0.0
        prevMaxNumber = 0

        while True:
            # gameEnv.PrintGrid()

            action = agent.get_action(state)

            # action = agent.get_action(state)
            (moveScore, isValid) = gameEnv.Move(action + 1)

            next_state = gameEnv.GetFlatGrid()
            next_state = np.reshape(next_state, [1, state_size])

            if isValid:
                # Lenth of game award
                # reward = 10.0

                # # Rewards for single peak
                # mat = gameEnv.GetMatrix()
                # peaks = getPeaks(mat)
                # if len(peaks) == 1:
                #     reward += 10.0

                # Reward for step score
                reward += moveScore

                # Reward for New Max Number
                if gameEnv.GetMaxNumber() > prevMaxNumber:
                    reward += 10.0
                    prevMaxNumber = gameEnv.GetMaxNumber()

                gameEnv.AddNewNumber()
            else:
                reward = -50.0

            done = gameEnv.CheckGameOver()
            if done:
                reward = -100.0

            agent.append_sample(state, action, reward, next_state, done)
            # agent.learn(str(state), action, reward, str(next_state))
            agent.train_model()
            state = next_state

            if done:
                # gameEnv.PrintGrid()
                agent.update_target_model()

                scores.append(gameEnv.GetScore())
                episodes.append(e)

                pylab.plot(episodes, scores, 'b')
                pylab.savefig("2048_ddqn.png")

                # print("episode: {}/{}, score: {}, MaxNumber: {}, memory length: {}, e: {:.2}".format(e, EPISODES, gameEnv.GetScore(), 2**gameEnv.GetMaxNumber(), len(agent.memory), agent.epsilon))
                print("episode: {}/{}, score: {}, MaxNumber: {}, MemSize {}, e: {:.2}".format(e, EPISODES, gameEnv.GetScore(), 2**gameEnv.GetMaxNumber(), len(agent.memory), agent.epsilon))
                break

        # save the model
        if e % 50 == 0:
            agent.model.save_weights("2048_"+str(gridSize)+".h5")
