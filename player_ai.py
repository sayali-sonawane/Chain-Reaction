from board import Board
import random
import copy
import numpy as np


class AIPlay:

    def __init__(self, game_cr, training_dict=None):

        self.game = game_cr
        self.dummy_board = Board()
        self.discount = 0.5
        self.prev_move_1 = ''
        self.prev_move_2 = ''

        # learning mode
        if training_dict:
            self.value_dict = dict(training_dict)
            self.epsilon = 0.98
        else:
            self.value_dict = {}
            self.epsilon = 0.2

    # Get a random move to play
    # param player - player to be randomized
    # gets the available move and chooses a random move
    def get_random_move(self, player):
        states = self.get_possible_states(player.color)
        for i in states:
            rep = self.get_afterstate(player.color, i)
            rep = self.get_board_rep(rep)
            if rep not in self.value_dict:
                return i[0], i[-1]
            else:
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
    def get_move(self, player):
        value_addition = {}
        current_rep = self.get_board_rep(self.game.get_board())
        random_num = random.random()

        if player.color == 'red':
            if self.prev_move_1 == '':
                self.prev_move_1 = current_rep

            if self.prev_move_1 not in self.value_dict:
                self.value_dict[self.prev_move_1] = 0
        else:
            if self.prev_move_2 == '':
                self.prev_move_2 = current_rep

            if self.prev_move_2 not in self.value_dict:
                self.value_dict[self.prev_move_2] = 0

        if random_num < self.epsilon:

            states = self.get_possible_states(player.color)

            for state in states:
                after_state = self.get_afterstate(player.color, state)
                after_state_rep = self.get_board_rep(after_state)

                if after_state_rep != current_rep:
                    reward = self.get_afterstate_reward(current_rep, after_state_rep, player.color)
                    if after_state_rep in self.value_dict:
                        val = self.value_dict[after_state_rep]
                        value_addition[after_state_rep, state] = reward + self.value_dict[after_state_rep]
                    else:
                        value_addition[after_state_rep, state] = reward
            chosen_after_state_rep, chosen_after_state = max(value_addition, key=lambda key: value_addition[key])

        else:
            i, j = self.get_random_move(player)
            after_state = self.get_afterstate(player.color, (i, j))
            chosen_after_state = (i, j)
            chosen_after_state_rep = self.get_board_rep(after_state)
            reward = 0
            if chosen_after_state_rep != current_rep:
                reward = self.get_afterstate_reward(current_rep, chosen_after_state_rep, player.color)
            if chosen_after_state_rep in self.value_dict:
                val = self.value_dict[chosen_after_state_rep]
                value_addition[chosen_after_state_rep, (i, j)] = reward + self.value_dict[chosen_after_state_rep]
            else:
                value_addition[chosen_after_state_rep, (i, j)] = reward

        if player.color == 'red':
            bracket = value_addition[chosen_after_state_rep, chosen_after_state] - self.value_dict[self.prev_move_1]
            self.value_dict[self.prev_move_1] = self.value_dict[self.prev_move_1] + self.discount*bracket
            self.prev_move_1 = chosen_after_state_rep
        else:
            bracket = value_addition[chosen_after_state_rep, chosen_after_state] - self.value_dict[self.prev_move_2]
            self.value_dict[self.prev_move_2] = self.value_dict[self.prev_move_2] + self.discount*bracket
            self.prev_move_2 = chosen_after_state_rep
        return chosen_after_state[0], chosen_after_state[-1]

    def update(self, player):
        current_rep = self.get_board_rep(self.game.get_board())
        val = self.get_afterstate_reward(self.prev_move_2, current_rep, player.color)
        if self.prev_move_2 != '':
            if self.prev_move_2 in self.value_dict:
                self.value_dict[self.prev_move_2] = self.discount*val + self.value_dict[self.prev_move_2]
            else:
                self.value_dict[self.prev_move_2] = self.discount * val
            self.prev_move_2 = ''
        elif self.prev_move_1 != '':
            if self.prev_move_1 in self.value_dict:
                self.value_dict[self.prev_move_1] = self.discount*val + self.value_dict[self.prev_move_1]
            else:
                self.value_dict[self.prev_move_1] = self.discount * val
            self.prev_move_1 = ''


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
    def get_afterstate_reward(self, current_rep, afterstate_rep, player_col):
        if 'a' not in afterstate_rep and 'b' not in afterstate_rep and 'c' not in afterstate_rep:
            if player_col == 'green':
                if self.find_score(current_rep, player_col) != 0:
                    return 1000
                else:
                    return -0.1
            else:
                if self.find_score(current_rep, player_col) != 0:
                    return -1000
                else:
                    return -0.1
        elif 'x' not in afterstate_rep and 'y' not in afterstate_rep and 'z' not in afterstate_rep:
            if player_col == 'green':
                if self.find_score(current_rep, player_col) != 0:
                    return -1000
                else:
                    return -0.1
            else:
                if self.find_score(current_rep, player_col) != 0:
                    return 1000
                else:
                    return -0.1

        else:
            return -0.1

        # a = self.find_score(afterstate_rep, player_col)
        # b = self.find_score(current_rep, player_col)
        #
        # if a > b:
        #     k = (a - b)*2 + 10
        #     return k*0.5
        # if a <= b:
        #     k = (a - b)*2 - 10
        #     return k*0.5
        # return 0

    def find_score(self, afterstate_rep, player_col):
        rep = list(afterstate_rep)
        if player_col == 'green':
            score = rep.count('x') + rep.count('y')*3 + rep.count('z')*5
        else:
            score = rep.count('a') + rep.count('b')*3 + rep.count('c')*5
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

