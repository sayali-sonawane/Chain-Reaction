import utils
import random


class QValueAgent:
    def __init__(self, game, training, discount=0.6, learning_rate=0.9):
        self.discount = discount
        self.learning_rate = learning_rate
        self.q_values = training if training else {}
        self.game = game
        self.board = self.game.board

    def get_random_move(self, player):
        states = self.board.get_available_moves(player.color)
        return states[random.randrange(0, len(states))]

    def get_move(self, Q_player):
        """
            Gets the move according to the current state and the Q values.
        :return:
        """
        next_moves = self.board.get_available_moves(Q_player.color)
        current_board = self.board.get_board_rep()

        # If state does not exist, create one.
        if current_board not in self.q_values:
            self.q_values[current_board] = {}

        Q = {}

        # calculate Q value for each move. Take the move with the max Q value.
        for move in next_moves:
            board_after_move = self.board.get_dummy_board_after_move(move, Q_player.color)
            reward = self.get_reward_for_move(current_board, board_after_move)
            sample = reward

            # Implement look ahead.
            if board_after_move in self.q_values:
                sample = reward + self.get_max_q_value_for_state(board_after_move)

            # If next_state (action) does not exist for current state, initialize its value as 0.
            if board_after_move not in self.q_values[current_board]:
                self.q_values[current_board][board_after_move] = 0.0

            # Sample Based Q Learning to populate Q values.
            self.q_values[current_board][board_after_move] = self.learning_rate * sample + \
                (1 - self.learning_rate) * self.q_values[current_board][board_after_move]

            Q[move] = self.q_values[current_board][board_after_move]

        return utils.get_argmax_key(Q)

    def get_max_q_value_for_state(self, state):
        return max(self.q_values[state].values())

    def get_reward_for_move(self, current_board, board_after_move):
        return self.get_comparitive_reward(current_board, board_after_move)

    def get_comparitive_reward(self, current_rep, afterstate_rep):
        # Gives the expected immediate reward after the move
        if 'a' not in afterstate_rep and 'b' not in afterstate_rep and 'c' not in afterstate_rep:
            return 1000
        if 'x' not in afterstate_rep and 'y' not in afterstate_rep and 'z' not in afterstate_rep:
            return -1000

        a = self.find_score(afterstate_rep)
        b = self.find_score(current_rep)

        if a > b:
            return (a - b) * 2 + 10
        if a <= b:
            return (a - b) * 2 - 10
        return 0

    def find_score(self, afterstate_rep):
        rep = list(afterstate_rep)
        score = rep.count('x') + rep.count('y') * 3 + rep.count('z') * 5
        return score
