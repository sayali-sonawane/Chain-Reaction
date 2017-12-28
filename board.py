"""
    Board Module: defines the Board and the features required for the game.
"""
import copy
import numpy as np

signature_map = lambda player: 1 if player == 'green' else 0
player_map = lambda sign: 'green' if sign == 1 else 'red'

BLOCK_DEFAULT_COLOR = 'black'


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
        self.fresh_move = True

    def get_available_moves(self, player):
        """
            Gets available set of moves for a player
        :param player: Player(player.color) for whom available set of moves are returned.
        This player is represented by the color.
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

    def move(self, player, i, j, blocks=None):
        """
            Contains the Logic to make a move for the player,
            Populates the grid with the configuration after the move.

            The Logic is as follows:
            If a cell is loaded with a number of orbs equal to its critical mass,the stack explodes.
            To each of the orthogonally adjacent cells, an orb is added and the initial cell looses
            as many orbs as its critical mass. The explosions might result in overloading of an adjacent cell and
            the chain reaction of explosion continues until every cell is stable.
        :param player: Player who has to make a move
        :param i: Row of the board
        :param j: Column of the board
        """
        if not self.is_move_allowed(player, i, j):
            return False
        if self.board[i][j] != self.get_max_critical_mass_for_cell(i, j) - 1:
            self.fresh_move = True
            self.distribution[i][j] = signature_map(player)
            self.board[i][j] += 1

            if blocks:
                text = str(int(self.board[i][j]))
                blocks[i][j].configure(fg=player, text=text)

        else:
            self.fresh_move = False
            # Start chain reaction.
            self._chain(player, i, j, blocks)

        return True

    def _chain(self, player, i, j, blocks=None):
        if i < 0 or j < 0 or i == self.width or j == self.height:
            return

        critical_mass = self.get_max_critical_mass_for_cell(i, j)
        if self.board[i][j] == critical_mass - 1:
            self.board[i][j] = 0
            self.distribution[i][j] = np.nan

            if blocks:
                empty_block_text = ''
                blocks[i][j].configure(bg=BLOCK_DEFAULT_COLOR, text=empty_block_text)

            self._chain(player, i+1, j, blocks)
            self._chain(player, i, j+1, blocks)
            self._chain(player, i-1, j, blocks)
            self._chain(player, i, j-1, blocks)
        else:
            self.distribution[i][j] = signature_map(player)
            self.board[i][j] += 1

            if blocks:
                text = str(int(self.board[i][j]))
                blocks[i][j].configure(fg=player, text=text)

    def winner(self):
        """
            Winner is defined only when a chain rection occurs and
            the all the other player's orbs are destroyed.
        :return: {Boolean} If a winner exists else False.
        """

        player_1_count = 0
        player_2_count = 0

        if self.fresh_move:
            return False, False

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
        :return: {Boolean} True if the game is over else False
        """
        is_winner, _ = self.winner()
        return is_winner

    def reset(self):
        """
        Resets the Board.
        """
        self.board = np.zeros((self.width, self.height))
        self.distribution = np.ones((self.width, self.height)) * np.nan

    def give_board_status(self):
        return self.board, self.distribution

    def get_board_rep(self):
        """
            Creates the representation of the board, (state).
            1. a,b,c belonging to player one indicate 1,2,3 orbs respectively
            2. x,y,z belonging to player two indicate 1,2,3 orbs respectively
        :return: {String} Returns the representation
        """
        dummy_distribution, dummy_positions = self.give_board_status()
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

    def get_dummy_board_after_move(self, move, player):
        """
            Gets a dummy board rep after a certain move is played
        :param move: (i, j) Row and column number representing the move
        :param player: player playing the move. (player color is given)
        :return: Dummy board representation
        """
        dummy_board = copy.deepcopy(self)
        i, j = move
        dummy_board.move(player, i, j)

        return dummy_board
