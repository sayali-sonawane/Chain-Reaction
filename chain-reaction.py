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
    mode = 0
    training = None
    blocks = None
    iterations = 1000
    agent = None

    # Initailize Game
    game = Game(blocks, player_one, player_two)

    if mode == 0:
        with open('training_Q_values.pickle', 'rb') as handle:
            training = pickle.load(handle)

    print "training loaded"
    # Initialize Agents.
    value_agent = AIPlay(game, training)
    q_agent = QValueAgent(game, training)

    if mode == 2:
        agent = q_agent
    if mode == 1:
        agent = value_agent

    # Use previous training in testing mode
    if mode == 0:
        root = Tk.Tk()
        root.title("Chain Reaction Game")

        # Choose agent for testing.
        agent = q_agent
        blocks = initialize_tk_frame(root, q_agent)
        game.blocks = blocks
        root.mainloop()

    else:
        for _ in range(iterations):
            while True:
                print game.board.board
                print game.board.distribution
                if game.is_over():
                    _, winner = game.get_board().winner()
                    win_stats[winner] = win_stats[winner] + 1
                    game.reset()
                    break
                if game.get_current_player() == player_one:
                    i, j = agent.get_random_move(player_one)
                else:
                    agent.get_move(player_two)

                game.play(int(i), int(j))

        # If in training mode, dump all the training in a file
        if mode == 1:
            with open('training_value.pickle', 'wb') as handle:
                pickle.dump(value_agent.value_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        if mode == 2:
            with open('training_Q.pickle', 'wb') as handle:
                pickle.dump(q_agent.q_values, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print(win_stats)
