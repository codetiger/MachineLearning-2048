from gamelogic import *
from ddqn import DQNAgent
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras import backend as K
import gym
import numpy as np

EPISODES = 10000

if __name__ == "__main__":
    gridSize = 4
    gameEnv = GameLogic(gridSize)

    state_size = gridSize * gridSize
    action_size = 4
    agent = DQNAgent(state_size, action_size)

    # try:
    #     agent.load("2048.h5")
    # except IOError:
    #     pass

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
        reward = 0.0

        while True:
            # gameEnv.PrintGrid()
            action = agent.act(state)
            (moveScore, isValid) = gameEnv.Move(action + 1)

            next_state = gameEnv.GetFlatGrid()
            next_state = np.reshape(next_state, [1, state_size])

            prevMaxNumber = 0
            reward = -1.0

            if isValid:
                gameEnv.AddNewNumber()

            if moveScore:
                reward = moveScore / 2**10

            done = gameEnv.CheckGameOver()
            if done:
                reward = -1.0

            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                gameEnv.PrintGrid()
                agent.update_target_model()
                print("episode: {}/{}, score: {}, MaxNumber: {}, e: {:.2}".format(e, EPISODES, gameEnv.GetScore(), 2**gameEnv.GetMaxNumber(), agent.epsilon))
                break

        if len(agent.memory) > batch_size:
            agent.replay(batch_size)
        # if e % 10 == 0:
        #     agent.save("2048.h5")
