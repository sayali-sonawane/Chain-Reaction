import random
from board import Board

# Standard player playing with a greedy strategy
# Intended to be used as metric for evaluation of learning methods


class StdPlay:

    def __init__(self, game_cr):

        self.game = game_cr
        self.dummy_board = Board()

    def get_move(self, player):
        value_addition = {}
        current_rep = self.game.board.get_board_rep()
        states = self.get_possible_states(player.color)

        for state in states:
            after_state = self.game.board.get_dummy_board_after_move(state, player.color)
            after_state_rep = after_state.get_board_rep()
            if after_state_rep != current_rep:
                reward = self.get_afterstate_reward(current_rep, after_state_rep, player.color)
                value_addition[after_state_rep, state] = reward

        chosen_after_state_rep, chosen_after_state = max(value_addition, key=lambda key: value_addition[key])
        choices = []
        for item in value_addition:

            if value_addition[item] == value_addition[chosen_after_state_rep, chosen_after_state]:
                choices.append(item[-1])

        random_max_after_state = random.choice(choices)
        return random_max_after_state[0], random_max_after_state[-1]

    # Returns the possible states
    def get_possible_states(self, player):
        return (self.game.get_board()).get_available_moves(player)

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
            k = (a - b) * 2 + 10
            return k * 0.5
        if a <= b:
            k = (a - b) * 2 - 10
            return k * 0.5
        return 0

    def find_score(self, afterstate_rep, player_col):
        rep = list(afterstate_rep)
        if player_col == 'green':
            score = rep.count('x') + rep.count('y')*3 + rep.count('z')*5
        else:
            score = rep.count('a') + rep.count('b')*3 + rep.count('c')*5
        return score
