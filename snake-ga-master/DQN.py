from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
import random
import numpy as np
import pandas as pd
from operator import add
import collections

class DQNAgent(object):
    def __init__(self, params, num):
        self.reward = 0
        self.gamma = 0.9
        self.dataframe = pd.DataFrame()
        self.short_memory = np.array([])
        self.agent_target = 1
        self.agent_predict = 0
        self.learning_rate = params['learning_rate']        
        self.epsilon = 1
        self.actual = []
        self.first_layer = params['first_layer_size']
        self.second_layer = params['second_layer_size']
        self.third_layer = params['third_layer_size']
        self.memory = collections.deque(maxlen=params['memory_size'])
        self.weights1 = params['weights_path1']
        self.weights2 = params['weights_path2']
        self.load_weights = params['load_weights']
        self.num = num
        self.model = self.network()
        

    def network(self):
        model = Sequential()
        model.add(Dense(self.first_layer, activation='relu', input_dim=7))
        model.add(Dense(self.second_layer, activation='relu'))
        model.add(Dense(self.third_layer, activation='relu'))
        model.add(Dense(3, activation='softmax'))
        opt = Adam(self.learning_rate)
        model.compile(loss='mse', optimizer=opt)

        if self.load_weights:
            if self.num == 1:
                model.load_weights(self.weights1)
            elif self.num == 2:
                model.load_weights(self.weights2)
        return model
    
    def get_state(self, game, player1, player2):
        state = [
            (player1.x_change == 20 and player1.y_change == 0 and ((list(map(add, player1.position[-1], [20, 0])) in player1.position) or (list(map(add, player1.position[-1], [20, 0])) in player2.position) or
            player1.position[-1][0] + 20 >= (game.game_width - 20))) or (player1.x_change == -20 and player1.y_change == 0 and ((list(map(add, player1.position[-1], [-20, 0])) in player1.position) or (list(map(add, player1.position[-1], [-20, 0])) in player2.position) or
            player1.position[-1][0] - 20 < 20)) or (player1.x_change == 0 and player1.y_change == -20 and ((list(map(add, player1.position[-1], [0, -20])) in player1.position) or (list(map(add, player1.position[-1], [0, -20])) in player2.position) or
            player1.position[-1][-1] - 20 < 20)) or (player1.x_change == 0 and player1.y_change == 20 and ((list(map(add, player1.position[-1], [0, 20])) in player1.position) or (list(map(add, player1.position[-1], [0, 20])) in player2.position) or
            player1.position[-1][-1] + 20 >= (game.game_height-20))),  # danger straight

            (player1.x_change == 0 and player1.y_change == -20 and ((list(map(add,player1.position[-1],[20, 0])) in player1.position) or (list(map(add,player1.position[-1],[20, 0])) in player2.position) or
            player1.position[ -1][0] + 20 > (game.game_width-20))) or (player1.x_change == 0 and player1.y_change == 20 and ((list(map(add,player1.position[-1],
            [-20,0])) in player1.position) or  (list(map(add,player1.position[-1], [-20,0])) in player2.position) or player1.position[-1][0] - 20 < 20)) or (player1.x_change == -20 and player1.y_change == 0 and ((list(map(
            add,player1.position[-1],[0,-20])) in player1.position) or (list(map(add,player1.position[-1],[0,-20])) in player2.position) or player1.position[-1][-1] - 20 < 20)) or (player1.x_change == 20 and player1.y_change == 0 and (
            (list(map(add,player1.position[-1],[0,20])) in player1.position) or (list(map(add,player1.position[-1],[0,20])) in player2.position) or player1.position[-1][
             -1] + 20 >= (game.game_height-20))),  # danger right

             (player1.x_change == 0 and player1.y_change == 20 and ((list(map(add,player1.position[-1],[20,0])) in player1.position) or (list(map(add,player1.position[-1],[20,0])) in player2.position) or
             player1.position[-1][0] + 20 > (game.game_width-20))) or (player1.x_change == 0 and player1.y_change == -20 and ((list(map(
             add, player1.position[-1],[-20,0])) in player1.position) or (list(map(add, player1.position[-1],[-20,0])) in player2.position) or player1.position[-1][0] - 20 < 20)) or (player1.x_change == 20 and player1.y_change == 0 and (
            (list(map(add,player1.position[-1],[0,-20])) in player1.position) or (list(map(add,player1.position[-1],[0,-20])) in player2.position) or player1.position[-1][-1] - 20 < 20)) or (
            player1.x_change == -20 and player1.y_change == 0 and ((list(map(add,player1.position[-1],[0,20])) in player1.position) or (list(map(add,player1.position[-1],[0,20])) in player2.position) or
            player1.position[-1][-1] + 20 >= (game.game_height-20))), #danger left


            player1.x_change == -20,  # move left
            player1.x_change == 20,  # move right
            player1.y_change == -20,  # move up
            player1.y_change == 20,  # move down
            ]

        for i in range(len(state)):
            if state[i]:
                state[i]=1
            else:
                state[i]=0

        return np.asarray(state)

    def set_reward(self, player, crash):
        self.reward = 0
        if crash:
            self.reward = 0
            return self.reward
        else:
            self.reward = 1
        return self.reward

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay_new(self, memory, batch_size):
        if len(memory) > batch_size:
            minibatch = random.sample(memory, batch_size)
        else:
            minibatch = memory
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
            target_f = self.model.predict(np.array([state]))
            target_f[0][np.argmax(action)] = target
            self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)

    def train_short_memory(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = reward + self.gamma * np.amax(self.model.predict(next_state.reshape((1, 7)))[0])
        target_f = self.model.predict(state.reshape((1, 7)))
        target_f[0][np.argmax(action)] = target
        self.model.fit(state.reshape((1, 7)), target_f, epochs=1, verbose=0)