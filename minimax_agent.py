"""
    This module implements the Minimax algorithm for chain reaction.

    :example: An instance of the class can be made in the following way:

"""
from board import signature_map

switch_player = lambda x: 'green' if x == 'red' else 'red'
switch_agent_type = lambda x: max if x == min else min


class MinimaxAgent:
    def __init__(self, board):
        self.board = board
        self.depth = 1

    def get_best_move(self, agent_type):
        return float('-inf') if agent_type == max else float('inf')

    def get_move(self, player, agent_type):
        return self.minimax(player.color, self.board, agent_type, 0)

    def minimax(self, player, board, agent_type, depth):
        moves = board.get_available_moves(player)

        is_winner, won_by = board.winner()
        if is_winner:
            # If Agent has won, return reward 1000
            if signature_map(won_by) == 1:
                return 1000
            # Negative reward if Agent does not win
            return -1000

        depth = depth + 1

        if depth > self.depth:
            return -1

        reward_dict = {}

        best_value = self.get_best_move(agent_type)

        # Get rewards for all moves.
        for move in moves:
            board_after_move = board.get_dummy_board_after_move(move, player)
            reward = self.minimax(switch_player(player), board_after_move, switch_agent_type(agent_type), depth)

            best_value = agent_type(best_value, reward)

            reward_dict[move] = reward

        # Find move that gives the max or min reward (from the available moves) according to the agent type.
        return best_value
