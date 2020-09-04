import os
import pygame
import argparse
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from DQN import DQNAgent
from random import randint
from keras.utils import to_categorical

#################################
#   Define parameters manually  #
#################################
def define_parameters():
    params = dict()
    params['epsilon_decay_linear'] = 1/75
    params['learning_rate'] = 0.0005
    params['first_layer_size'] = 150   # neurons in the first layer
    params['second_layer_size'] = 150   # neurons in the second layer
    params['third_layer_size'] = 150    # neurons in the third layer
    params['episodes'] = 80            
    params['memory_size'] = 2500
    params['batch_size'] = 500
    params['weights_path1'] = 'weights/weights.hdf5'
    params['weights_path2'] = 'weights/weights2.hdf5'
    params['load_weights'] = True
    params['train'] = False
    return params



class Game:
    def __init__(self, game_width, game_height):
        pygame.display.set_caption('SnakeGen')
        self.game_width = game_width
        self.game_height = game_height
        self.gameDisplay = pygame.display.set_mode((game_width, game_height + 60))
        self.bg = pygame.image.load("img/background.png")
        self.crash = False
        self.score1 = 0
        self.score2 = 0


class Player(object):
    def __init__(self, game, x, y):

        self.x = x
        self.y = y
        self.position = []
        self.position.append([self.x, self.y])
        self.image = pygame.image.load('img/snakeBody.png')
        self.x_change = 20
        self.y_change = 0
        self.crash = False

    def grow(self):
        self.position.append([self.x, self.y])

    def do_move(self, move, x, y, game, agent, player2):
        move_array = [self.x_change, self.y_change]


        if np.array_equal(move, [1, 0, 0]):
            move_array = self.x_change, self.y_change
        elif np.array_equal(move, [0, 1, 0]) and self.y_change == 0:  # right - going horizontal
            move_array = [0, self.x_change]
        elif np.array_equal(move, [0, 1, 0]) and self.x_change == 0:  # right - going vertical
            move_array = [-self.y_change, 0]
        elif np.array_equal(move, [0, 0, 1]) and self.y_change == 0:  # left - going horizontal
            move_array = [0, -self.x_change]
        elif np.array_equal(move, [0, 0, 1]) and self.x_change == 0:  # left - going vertical
            move_array = [self.y_change, 0]
        self.x_change, self.y_change = move_array
        self.x = x + self.x_change
        self.y = y + self.y_change

        if self.x < 20 or self.x > game.game_width - 40 \
                or self.y < 20 \
                or self.y > game.game_height - 40 \
                or [self.x, self.y] in self.position or [self.x, self.y] in player2.position:
            self.crash = True

        if not self.crash:
            self.grow()

    def display_player(self, x, y, game):
        self.position[-1][0] = x
        self.position[-1][1] = y

        if game.crash == False:
            for i in range(len(self.position)):
                x_temp, y_temp = self.position[len(self.position) - 1 - i]
                game.gameDisplay.blit(self.image, (x_temp, y_temp))










def get_record(score, record):
    if score >= record:
        return score
    else:
        return record


def display_ui(game, score1, score2, record1, record2):
    myfont = pygame.font.SysFont('Segoe UI', 20)
    myfont_bold = pygame.font.SysFont('Segoe UI', 20, True)
    text_score1 = myfont.render('SCORE1: ', True, (0, 0, 0))
    text_score_number1 = myfont.render(str(score1), True, (0, 0, 0))
    text_highest1 = myfont.render('HIGHEST SCORE1: ', True, (0, 0, 0))
    text_highest_number1 = myfont_bold.render(str(record1), True, (0, 0, 0))

    text_score2 = myfont.render('SCORE2: ', True, (0, 0, 0))
    text_score_number2 = myfont.render(str(score2), True, (0, 0, 0))
    text_highest2 = myfont.render('HIGHEST SCORE2: ', True, (0, 0, 0))
    text_highest_number2 = myfont_bold.render(str(record2), True, (0, 0, 0))

    game.gameDisplay.blit(text_score1, (45, 600))
    game.gameDisplay.blit(text_score_number1, (120, 600))
    game.gameDisplay.blit(text_highest1, (450, 600))
    game.gameDisplay.blit(text_highest_number1, (610, 600))

    game.gameDisplay.blit(text_score2, (45, 500))
    game.gameDisplay.blit(text_score_number2, (120, 500))
    game.gameDisplay.blit(text_highest2, (450, 500))
    game.gameDisplay.blit(text_highest_number2, (610, 500))




def display(player1, player2, game, record1, record2):
    game.gameDisplay.fill((255, 255, 255))
    display_ui(game, game.score1, game.score2, record1, record2)
    player1.display_player(player1.position[-1][0], player1.position[-1][1], game)
    player2.display_player(player2.position[-1][0], player2.position[-1][1], game)
    update_screen()



def update_screen():
    pygame.display.update()


def initialize_game(player1, player2, game, agent1, agent2, batch_size):
    state_init11 = agent1.get_state(game, player1, player2)
    state_init21 = agent2.get_state(game, player2, player1)  # [0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0]
    action = [1, 0, 0]
    player1.do_move(action, player1.x, player1.y, game, agent1, player2)
    player2.do_move(action, player2.x, player2.y, game, agent2, player1)
    state_init12 = agent1.get_state(game, player1, player2)
    state_init22 = agent2.get_state(game, player2, player1)
    reward1 = agent1.set_reward(player1, player1.crash)
    reward2 = agent2.set_reward(player2, player2.crash)
    agent1.remember(state_init11, action, reward1, state_init12, player1.crash)
    agent1.replay_new(agent1.memory, batch_size)
    agent2.remember(state_init21, action, reward2, state_init22, player2.crash)
    agent2.replay_new(agent2.memory, batch_size)


def plot_seaborn(array_counter, array_score):
    sns.set(color_codes=True)
    ax = sns.regplot(
        np.array([array_counter])[0],
        np.array([array_score])[0],
        color="b",
        x_jitter=.1,
        line_kws={'color': 'green'}
    )
    ax.set(xlabel='games', ylabel='score')
    plt.show()


def run(display_option, speed, params):
    pygame.init()
    agent1 = DQNAgent(params, 1)
    agent2 = DQNAgent(params, 2)
    weights_filepath1 = params['weights_path1']
    weights_filepath2 = params['weights_path2']


    counter_games = 0
    record1 = 0
    record2 = 0
    while counter_games < params['episodes']:
        if params['load_weights']:
            agent1.model.load_weights(weights_filepath1)
            agent2.model.load_weights(weights_filepath2)
            print("weights loaded")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # Initialize classes
        game = Game(900, 600)
        player1 = Player(game, 300, 300)
        player2 = Player(game, 600, 300)

        # Perform first move
        initialize_game(player1, player2, game, agent1, agent2, params['batch_size'])
        if display_option:
            display(player1, player2, game, record1, record2)

        while not game.crash:
            if not params['train']:
                agent1.epsilon = 0
                agent2.epsilon = 0
            else:
                # agent.epsilon is set to give randomness to actions
                agent1.epsilon = 1 - (counter_games * params['epsilon_decay_linear'])
                agent2.epsilon = 1 - (counter_games * params['epsilon_decay_linear'])

            # get old state
            state_old1 = agent1.get_state(game, player1, player2)
            state_old2 = agent2.get_state(game, player2, player1)

            # perform random actions based on agent.epsilon, or choose the action
            if randint(0, 1) < agent1.epsilon:
                final_move1 = to_categorical(randint(0, 2), num_classes=3)
            else:
                # predict action based on the old state
                prediction1 = agent1.model.predict(state_old1.reshape((1, 7)))
                final_move1 = to_categorical(np.argmax(prediction1[0]), num_classes=3)

            if randint(0, 1) < agent2.epsilon:
                final_move2 = to_categorical(randint(0, 2), num_classes=3)
            else:
                # predict action based on the old state
                prediction2 = agent2.model.predict(state_old2.reshape((1, 7)))
                final_move2 = to_categorical(np.argmax(prediction2[0]), num_classes=3)

            # perform new move and get new state
            player1.do_move(final_move1, player1.x, player1.y, game, agent1, player2)
            player2.do_move(final_move2, player2.x, player2.y, game, agent2, player1)
            state_new1 = agent1.get_state(game, player1, player2)
            state_new2 = agent2.get_state(game, player2, player1)
            # set reward for the new state
            reward1 = agent1.set_reward(player1, player1.crash)
            reward2 = agent2.set_reward(player2, player2.crash)

            if params['train']:
                # train short memory base on the new action and state
                agent1.train_short_memory(state_old1, final_move1, reward1, state_new1, player1.crash)
                # store the new data into a long term memory
                agent1.remember(state_old1, final_move1, reward1, state_new1, player1.crash)
                agent2.train_short_memory(state_old2, final_move2, reward2, state_new2, player2.crash)
                # store the new data into a long term memory
                agent2.remember(state_old2, final_move2, reward2, state_new2, player2.crash)
            game.score1 += reward1
            game.score2 += reward2
            record1 = get_record(game.score1, record1)
            record2 = get_record(game.score2, record2)
            if display_option:
                display(player1, player2, game, record1, record2)
                pygame.time.wait(speed)
            if player1.crash and player2.crash:
                game.crash = True

        counter_games += 1
        game.crash = False
        player1.crash = False
        player2.crash = False
        print("score1: " + str(game.score1) + "/n")
        print("score2: " + str(game.score2) + "/n")
        if params['train'] and counter_games % 10 == 0:
            agent1.model.save_weights(params['weights_path1'])
            agent2.model.save_weights(params['weights_path2'])
            print("weights saved")
    if params['train']:
        agent1.model.save_weights(params['weights_path1'])
        agent2.model.save_weights(params['weights_path2'])



if __name__ == '__main__':
    # Set options to activate or deactivate the game view, and its speed
    pygame.font.init()
    parser = argparse.ArgumentParser()
    params = define_parameters()
    parser.add_argument("--display", type=bool, default=True)
    parser.add_argument("--speed", type=int, default=50)
    args = parser.parse_args()
    params['bayesian_optimization'] = False    # Use bayesOpt.py for Bayesian Optimization
    run(args.display, args.speed, params)
