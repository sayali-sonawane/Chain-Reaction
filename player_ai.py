from board import Board
import random
import copy
import numpy as np


class AIPlay:

    def __init__(self, game_cr, training_dict=None):

        self.game = game_cr
        self.dummy_board = Board()
        self.discount = 0.5
        # learning mode
        if training_dict:
            self.value_dict = dict(training_dict)
        else:
            self.value_dict = {}

    # Get a random move to play
    # param player - player to be randomized
    # gets the available move and chooses a random move
    def get_random_move(self, player):
        states = self.get_possible_states(player.color)
        move = states[random.randrange(0, len(states))]
        return move[0], move[-1]

    # Get a move to play from the ai
    # param player - player to be ai'd
    # Steps -
    # 1. Creates a value addition dictionary
    # 2. Gets the current representation of the board
    # 3. Gets the possible moves at the current board state
    # 4. For each move, computes the afterstate, board representation and expected value addition
    # 5. Chooses the move with best value addition
    # 6. Updates the value dictionary
    def get_ai_move(self, player):
        value_addition = {}
        current_rep = self.get_board_rep(self.game.get_board())

        if current_rep not in self.value_dict:
            self.value_dict[current_rep] = 0

        states = self.get_possible_states(player.color)

        for state in states:
            after_state = self.get_afterstate(player.color, state)
            after_state_rep = self.get_board_rep(after_state)

            if after_state_rep != current_rep:
                reward = self.get_afterstate_reward(current_rep, after_state_rep)
                if after_state_rep in self.value_dict:
                    value_addition[after_state_rep, state] = reward + self.value_dict[after_state_rep]
                else:
                    value_addition[after_state_rep, state] = reward

        chosen_after_state_rep, chosen_after_state = max(value_addition, key=lambda key: value_addition[key])
        bracket = value_addition[chosen_after_state_rep, chosen_after_state] - self.value_dict[current_rep]
        self.value_dict[current_rep] = self.value_dict[current_rep] + self.discount*bracket

        return chosen_after_state[0], chosen_after_state[-1]

    # Returns the possible states
    def get_possible_states(self, player):
        return (self.game.get_board()).get_available_moves(player)

    # Creates the representation of the board to be stored in the value dictionary
    # a,b,c belonging to player one indicate 1,2,3 orbs respectively
    # x,y,z belonging to player two indicate 1,2,3 orbs respectively
    def get_board_rep(self, board):
        dummy_distribution, dummy_positions = board.give_board_status()
        dummy_positions = np.ndarray.flatten(dummy_positions)
        dummy_distribution = np.ndarray.flatten(dummy_distribution)
        board_rep = [0]*len(dummy_positions)
        for index, position in enumerate(dummy_positions):
            if position == 0:
                if dummy_distribution[index] == 1:
                    board_rep[index] = 'a'
                elif dummy_distribution[index] == 2:
                    board_rep[index] = 'b'
                elif dummy_distribution[index] == 3:
                    board_rep[index] = 'c'
            if position == 1:
                if dummy_distribution[index] == 1:
                    board_rep[index] = 'x'
                elif dummy_distribution[index] == 2:
                    board_rep[index] = 'y'
                elif dummy_distribution[index] == 3:
                    board_rep[index] = 'z'

        rep = "".join(str(x) for x in board_rep)
        return rep

    # Gives the expected immediate reward after the move
    def get_afterstate_reward(self, current_rep, afterstate_rep):
        if 'a' not in afterstate_rep and 'b' not in afterstate_rep and 'c' not in afterstate_rep:
            return 1000
        if 'x' not in afterstate_rep and 'y' not in afterstate_rep and 'z' not in afterstate_rep:
            return -1000

        a = self.find_score(afterstate_rep)
        b = self.find_score(current_rep)

        if a > b:
            return (a - b)*2 + 10
        if a <= b:
            return (a - b)*2 - 10
        return 0

    def find_score(self, afterstate_rep):
        rep = list(afterstate_rep)
        score = rep.count('x') + rep.count('y')*3 + rep.count('z')*5
        return score

    # Gives the afterstate after a certain player plays a move
    # param player - the player who makes the move
    # param move - the actual move
    # Steps:
    # 1. Create a deep copy of the current board state
    # 2. Check if the move is allowed and make the move, This is equivalent to simulating a move on actual board
    # 3. Return the afterstate board
    def get_afterstate(self, player, move):
        self.dummy_board = copy.deepcopy(self.game.get_board())
        if self.dummy_board.is_move_allowed(player, move[0], move[-1]):
            self.dummy_board.move(player, move[0], move[-1])
        return self.dummy_board

