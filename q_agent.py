import utils
import random
import numpy as np

from minimax_agent import MinimaxAgent

LOSING_REWARD = -1000


class QValueAgent:
    def __init__(self, game, training, discount=0.6, learning_rate=0.8, decay=0.999995, epsilon=0.8):
        self.discount = discount
        self.learning_rate = learning_rate
        self.decay = decay
        self.epsilon = epsilon
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

        Q = {}
        default_Q_value = 1

        # If state does not exist, create one.
        if current_board not in self.q_values:
            self.q_values[current_board] = {}

        # Explore according to epsilon.
        if np.random.uniform() < self.epsilon:
            unexplored_moves = self.get_unexplored_states(next_moves, Q_player)
            move = next_moves[random.randrange(0, len(next_moves))]
            if unexplored_moves:
                print "hereeeee"
                move = next_moves[random.randrange(0, len(unexplored_moves))]
            board_after_move = self.board.get_dummy_board_after_move(move, Q_player.color)
            self.calc_q_value(current_board, default_Q_value, board_after_move)
            self.decay_constants()
            return move

        # calculate Q value for each move. Take the move with the max Q value.
        for move in next_moves:
            board_after_move = self.board.get_dummy_board_after_move(move, Q_player.color)
            Q[move] = self.calc_q_value(current_board, default_Q_value, board_after_move)

        self.decay_constants()

        return utils.get_rand_argmax_key(Q)

    def get_unexplored_states(self, next_moves, Q_player):
        unexplored_states = [move for move in next_moves
                             if self.board.get_dummy_board_after_move(move, Q_player.color) not in self.q_values]

        return unexplored_states

    def calc_q_value(self, current_board, default_Q_value, board_after_move):
        minimax_reward = MinimaxAgent(board_after_move).get_move(self.game.other_player, min)

        sample = minimax_reward

        board_after_move = board_after_move.get_board_rep()
        # Implement look ahead.
        if board_after_move in self.q_values:
            sample = minimax_reward + self.get_max_q_value_for_state(board_after_move)

        # If next_state (action) does not exist for current state, initialize its value as 0.
        if board_after_move not in self.q_values[current_board]:
            self.q_values[current_board][board_after_move] = default_Q_value

        # Sample Based Q Learning to populate Q values.
        self.q_values[current_board][board_after_move] = self.learning_rate * sample + \
                                                         (1 - self.learning_rate) * self.q_values[current_board][
                                                             board_after_move]

        return self.q_values[current_board][board_after_move]

    def decay_constants(self):
        """
        decays the learning rate and exploration factor.
        """
        self.learning_rate = self.learning_rate * self.decay
        # self.epsilon = self.epsilon * self.decay

    def get_max_q_value_for_state(self, state):
        return max(self.q_values[state].values())
