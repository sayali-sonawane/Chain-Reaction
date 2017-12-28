import utils
import random
import numpy as np

from minimax_agent import MinimaxAgent


class QValueAgent:
    def __init__(self, game, training, discount=0.9, learning_rate=0.8, decay=0.99995, epsilon=0.8):
        self.discount = discount
        self.learning_rate = learning_rate
        self.decay = decay
        self.epsilon = epsilon
        self.q_values = training if training else {}
        self.game = game
        self.board = self.game.board
        self.prev_board = None

    def get_random_move(self, player):
        states = self.board.get_available_moves(player.color)
        return states[random.randrange(0, len(states))]

    def get_move(self, Q_player):
        """
            Gets the move according to the current state(board state on which agent action is played)
            and the Q values.
        :return: Move generated by the Q values.
        """

        next_moves = self.board.get_available_moves(Q_player.color)
        current_board = self.board.get_board_rep()

        if not self.prev_board:
            self.prev_board = current_board

        Q = {}
        default_Q_value = 1

        # If state does not exist, create one.
        if self.prev_board not in self.q_values:
            self.q_values[self.prev_board] = {}

        # Explore according to epsilon. (for exploration)
        if np.random.uniform() < self.epsilon:
            unexplored_moves = self.get_unexplored_states(next_moves, Q_player)
            move = next_moves[random.randrange(0, len(next_moves))]
            if unexplored_moves:
                move = next_moves[random.randrange(0, len(unexplored_moves))]

            board_after_move = self.board.get_dummy_board_after_move(move, Q_player.color)
            self.calc_q_value(default_Q_value, board_after_move, Q_player)

            self.prev_board = board_after_move.get_board_rep()
            return move

        # calculate Q value for each move. Take the move with the max Q value.
        for move in next_moves:
            board_after_move = self.board.get_dummy_board_after_move(move, Q_player.color)
            Q[move, board_after_move] = self.calc_q_value(default_Q_value, board_after_move, Q_player)

        move_chosen, board_chosen = utils.get_rand_argmax_key(Q)
        self.prev_board = board_chosen

        return move_chosen

    def get_unexplored_states(self, next_moves, Q_player):
        """
            Gets moves/ states for which the Q values dictionary doesn't have an entry.
            This is done to get greater exploration.
        :param next_moves: List of available moves the Q player can take.
        :param Q_player: {Player} player for whom unexplored moves are returned.
        :return: {List} unexplored states/ moves.
        """
        unexplored_states = [move for move in next_moves
                             if self.board.get_dummy_board_after_move(move, Q_player.color) not in self.q_values]

        return unexplored_states

    def calc_q_value(self, default_Q_value, board_after_move, Q_player):
        """
            Calculated Q value based on the temporal difference method.
            The formula for calculation is:
                Q(s, a) = alpha * sample + (1 - alpha) * Q(s, a)

            where sample = Reward + gamma * (max(Q(s, a'))

        :param default_Q_value: Default Q value to be assigned in case there is no entry in the Q dictionary for
            a particular state.
        :param board_after_move: {Board} Instance of the Board class after a move has been played on the current board.
        :param Q_player: {Player} Player for which Q values are being calculated.

        :return: Q values of the action {move} for the current board.
        """

        # Gets minimax reward implementing one step look ahead.
        minimax_reward = MinimaxAgent(board_after_move).get_move(self.game.other_player, min)
        sample = minimax_reward

        board_after_move = board_after_move.get_board_rep()
        # Implement look ahead.
        if board_after_move in self.q_values:
            sample = minimax_reward + self.get_max_q_value_for_state(board_after_move)

        # If next_state (action) does not exist for current state, initialize its value as 0.
        if board_after_move not in self.q_values[self.prev_board]:
            self.q_values[self.prev_board][board_after_move] = default_Q_value

        # Sample Based Q Learning to populate Q values.
        self.q_values[self.prev_board][board_after_move] = self.learning_rate * sample + \
                                                         (1 - self.learning_rate) * self.q_values[self.prev_board][
                                                             board_after_move]

        return self.q_values[self.prev_board][board_after_move]

    def decay_constants(self):
        """
        decays the learning rate and exploration factor.
        """
        self.learning_rate = self.learning_rate * self.decay
        # self.epsilon = self.epsilon * self.decay

    def get_max_q_value_for_state(self, state):
        return max(self.q_values[state].values())

    def get_comparitive_reward(self, Q_player):
        """
            Gets the reward for the current state.
            This function can be modified to get comparitive rewards
            (taking the next state and the current state)
        :param Q_player: {Player} player for whom the reward is returned.
        :return:
        """
        is_winner, won_by = self.board.winner()
        if is_winner:

            # If game is won by the Q agent
            if won_by == Q_player.color:
                return 1000

            # If game is won by the other player
            return -1000

        # reward for all moves except winning and losing.
        return -1

    def update(self, Q_player):
        """
            Updates the last move for the Q Player. (end state)
            The last move consists of no next state and only the reward (loosing or winning).

            The actions/ states for the q value for the last states consists only of the winning/ losing board
            as no other action can be taken after this.
        :param Q_player: {Player} Q Agent for which Q values have to be updated
        """
        # TODO: Handle this as the same case.

        # Get the reward for the current state.
        reward = self.get_comparitive_reward(Q_player)
        current_board = self.board.get_board_rep()
        sample = reward

        if self.prev_board not in self.q_values:
            self.q_values[self.prev_board] = {}

        if current_board not in self.q_values[self.prev_board]:
            self.q_values[self.prev_board][current_board] = 1.0

        self.q_values[self.prev_board][current_board] = self.learning_rate * sample + \
                                                        (1 - self.learning_rate) * self.q_values[self.prev_board][
                                                            current_board]

        # Decay constants after completion of each game.
        self.decay_constants()
        self.prev_board = None