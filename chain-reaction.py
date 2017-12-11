"""
    Module: Chain Reaction.
    This module is used to train and test the chain reaction agent.

    mode = 0 - Testing mode
    mode = 1 - Training mode for Value Agent
    mode = 2 - Training mode for Q-Value Agent

    while in testing mode, the gui can be set up in the following way:
    (Sample Code for testing)

    player_one = Player("red")
    player_two = Player("green") or an Agent.
    root = Tk.Tk()
    root.title("Chain Reaction Game")

    game = Game(root, player_one, player_two)

    root.mainloop()

"""

from game import Game, Player
from player_ai import AIPlay

from q_agent import QValueAgent
from standard_player import StdPlay
from q_feature import qFeatureAgent

import pickle
import Tkinter as Tk

BLOCK_DEFAULT_COLOR = 'black'

WIDTH = 5
HEIGHT = 5


def initialize_tk_frame(root, agent):
    """
        Initializes Tk Frame for the game.
    :return:
    """
    frame = Tk.Frame(root)
    frame.grid()

    blocks = [[None for _ in range(HEIGHT)] for _ in range(WIDTH)]

    for i in range(WIDTH):
        for j in range(HEIGHT):
            blocks[i][j] = Tk.Button(frame, height=3, width=3, text="", bg=BLOCK_DEFAULT_COLOR,
                                     command=lambda i=i, j=j: game.handle_move(blocks[i][j], agent))
            blocks[i][j].grid(row=i, column=j)

    reset_button = Tk.Button(text="Reset", command=game.reset())
    reset_button.grid(row=5)

    return blocks


if __name__ == "__main__":

    player_one = Player("red")
    player_two = Player("green")

    win_stats = {'red': 0, 'green': 0}

    # initialize Configurations for Game.
    # mode = 0 - Testing
    # mode = 1 - Training
    # mode = 2 - AI_testing
    # player = 0 - Q_agent
    # player = 1 - Value_agent

    mode = 2
    player = 4
    training = None
    blocks = None
    iterations = 100
    agent = None
    agent_1 = None
    agent_2 = None
    feature_weight = None

    # Initialize Game
    game = Game(blocks, player_one, player_two, WIDTH, HEIGHT)

    # If in Testing mode, load the training data
    if mode != 1 and player != 4:
        # load value agent training
        if player == 1:
            with open('training_10th.pickle', 'rb') as handle:
                training = pickle.load(handle)
                print(len(training))
                #print(training)
        elif player == 3:
            with open('training_self.pickle', 'rb') as handle:
                training = pickle.load(handle)
                print(len(training))
        # load q agent training
        else:
            with open('training_Q.pickle', 'rb') as handle:
                training = pickle.load(handle)

    print "training loaded"
    # Initialize Agents.

    value_agent = AIPlay(game, training)
    value_agent_op = AIPlay(game, training)
    q_agent = QValueAgent(game, training)
    q_feature = qFeatureAgent(game, feature_weight)
    std_agent = StdPlay(game)
    # Set Player agents
    if player == 0:
        agent = q_agent
    elif player == 1:
        agent = value_agent
        agent_1 = std_agent
    elif player == 2:
        agent_1 = value_agent
        agent_2 = q_agent
    elif player == 4:
        agent = q_feature
        agent_1 = std_agent
    else:
        agent = value_agent

    # Use previous training in testing mode
    if mode == 0:
        root = Tk.Tk()
        root.title("Chain Reaction Game")

        # Choose agent for testing.
        blocks = initialize_tk_frame(root, agent)
        game.blocks = blocks
        root.mainloop()

    else:
        for i in range(iterations):
            print(i)
            while True:
                print game.board.board
                print game.board.distribution
                if game.is_over():
                    _, winner = game.get_board().winner()
                    win_stats[winner] = win_stats[winner] + 1
                    agent.update(player_two)
                    game.reset()
                    break
                if game.get_current_player() == player_one:
                    if player == 2:
                        i, j = agent_1.get_move(player_one)
                    elif player == 3:
                        i, j = agent.get_move(player_one)
                    elif player == 1:
                        i, j = agent_1.get_move(player_one)
                    elif player == 4:
                        i, j = agent_1.get_move(player_one)
                    else:
                        i, j = agent.get_random_move(player_one)
                else:
                    if player == 2:
                        i, j = agent_2.get_move(player_two)
                    elif player == 3:
                        i, j = agent.get_move(player_two)
                    elif player == 1:
                        i, j = agent.get_move(player_two)
                    else:
                        i, j = agent.get_move(player_two)
                game.play(int(i), int(j))

        # If all modes, dump all the training in a file
    if mode != 5 and player != 4:
        if player == 1:
            # save value agent training
            with open('training_10th.pickle', 'wb') as handle:
                pickle.dump(value_agent.value_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

        elif player == 3:
            with open('training_self.pickle', 'wb') as handle:
                pickle.dump(value_agent.value_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            # save q_agent training
            with open('training_Q.pickle', 'wb') as handle:
                pickle.dump(q_agent.q_values, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print(win_stats)
