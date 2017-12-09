from board import Board
import copy
import numpy as np

# Standard player playing with a greedy strategy
# Intended to be used as metric for evaluation of learning methods


class StdPlay:

    def __init__(self, game_cr):

        self.game = game_cr
        self.dummy_board = Board()

    def get_move(self, player):
        value_addition = {}
        current_rep = self.get_board_rep(self.game.get_board())
        states = self.get_possible_states(player.color)

        for state in states:
            after_state = self.get_afterstate(player.color, state)
            after_state_rep = self.get_board_rep(after_state)
            if after_state_rep != current_rep:
                reward = self.get_afterstate_reward(current_rep, after_state_rep, player.color)
                value_addition[after_state_rep, state] = reward

        chosen_after_state_rep, chosen_after_state = max(value_addition, key=lambda key: value_addition[key])
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
        board_rep = [0] * len(dummy_positions)
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
    def get_afterstate_reward(self, current_rep, afterstate_rep, player_col):
        if 'a' not in afterstate_rep and 'b' not in afterstate_rep and 'c' not in afterstate_rep:
            if player_col == 'green':
                if self.find_score(current_rep, player_col) != 0:
                    return 1000
            else:
                if self.find_score(current_rep, player_col) != 0:
                    return -1000
        if 'x' not in afterstate_rep and 'y' not in afterstate_rep and 'z' not in afterstate_rep:
            if player_col == 'green':
                if self.find_score(current_rep, player_col) != 0:
                    return -1000
            else:
                if self.find_score(current_rep, player_col) != 0:
                    return 1000

        a = self.find_score(afterstate_rep, player_col)
        b = self.find_score(current_rep, player_col)

        if a > b:
            k = (a - b)*2 + 10
            return k*0.5
        if a <= b:
            k = (a - b)*2 - 10
            return k*0.5
        return 0

    def find_score(self, afterstate_rep, player_col):
        rep = list(afterstate_rep)
        if player_col == 'green':
            score = rep.count('x') + rep.count('y')*3 + rep.count('z')*5
        else:
            score = rep.count('a') + rep.count('b')*3 + rep.count('c')*5
        return score

    def get_afterstate(self, player, move):
        self.dummy_board = copy.deepcopy(self.game.get_board())
        if self.dummy_board.is_move_allowed(player, move[0], move[-1]):
            self.dummy_board.move(player, move[0], move[-1])
        return self.dummy_board

