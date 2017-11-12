import numpy as np

signature_map = lambda player: 1 if player == 'green' else 0
player_map = lambda sign: 'green' if sign == 1 else 'red'


class Board:
    """
        Defines the Board for Chain-Reaction
    """

    def __init__(self, width=5, height=5):
        self.width = width
        self.height = height
        self.board = np.zeros((self.width, self.height))

        # indicates which player places his orb in a cell.
        # 1 - player 1
        # 2 - player 2
        self.distribution = np.ones((self.width, self.height)) * np.nan

    def get_available_moves(self, player):
        """
            Gets available set of moves for a player
        :param player: Player for whom available set of moves are returned
        :return: {List} Available set of moves for a player.
        """
        return [(i, j) for i in range(self.width) for j in range(self.height)
                if self.is_move_allowed(player, i, j)]

    def get_max_critical_mass_for_cell(self, i, j):
        """
            Returns Maximum Critical Mass for a cell
        :param i: Row number of the cell
        :param j: Column number of the cell
        :return: {Integer} Maximum Critical Mass for a cell.
        """
        # Corner Points
        if (i == 0 and j == 0) or (i == 0 and j == self.height) or (i == self.width and j == 0) or \
                (i == self.width and j == self.height):
            return 2
        # Cells on the edge
        elif i == 0 or i == self.width or j == 0 or j == self.height:
            return 3
        # All Other Points
        else:
            return 4

    def is_move_allowed(self, player, i, j):
        """
            Indicates whether a move is allowed for a player or not
            A player can make a move to those cells which are either empty or
            have been previously occupied by the player himself.
        :param player: Player who has to make a move
        :param i: Row of the cell
        :param j: Column of the cell
        :return: {Boolean} True if move is allowed else False.
        """
        player = signature_map(player)
        return np.isnan(self.distribution[i][j]) or self.distribution[i][j] == player

    def move(self, player, i, j):
        if not self.is_move_allowed(player, i, j):
            return False

        critical_mass = self.get_max_critical_mass_for_cell(i, j)

        if self.board[i][j] == critical_mass - 1:
            # Start Chain Reaction
            pass
        else:
            self.board[i][j] += 1

    def chain(self):
        pass

    def reward(self):
        pass

    def is_winner(self):
        player_1_count = 0
        player_2_count = 0
        for i in range(self.width):
            for j in range(self.height):
                if self.distribution[i][j] == 1:
                    player_1_count += 1
                elif self.distribution[i][j] == 0:
                    player_2_count += 1

        if not player_1_count and player_2_count:
            return True, player_map(0)
        if not player_2_count and player_1_count:
            return True, player_map(1)

        return False, False

    def is_over(self):
        """
            Indicates if the Game is Over.
        :return:
        """
        return self.is_winner()

    def reset(self):
        """
        Resets the Board.
        """
        self.board = np.zeros((self.width, self.height))
        self.distribution = np.ones((self.width, self.height)) * np.nan
