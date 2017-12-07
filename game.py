"""
    Game Module: defines the game and the rules of the game.
"""
from board import Board
import Tkinter as tk

BLOCK_DEFAULT_COLOR = 'black'


class Player(object):
    """
        Defines a Player through a color code.
    """
    def __init__(self, color):
        self.color = color


class Game:
    """
        Defines a Two Player Game and it's rules
    """

    def __init__(self, root, player_one, player_two):
        self.player_one = player_one
        self.player_two = player_two
        self.current_player = self.player_one
        self.other_player = self.player_two
        self.board = Board()
        self.blocks = None
        if root:
            self.initialize_tk_frame(root)

    def play(self, i, j):
        is_legal_move = self.board.move(self.current_player.color, i, j, self.blocks)
        if not is_legal_move:
            return False

        if self.is_over():
            _, winner = self.board.winner()
            print '{} is the winner'.format(winner)
        else:
            self.switch_players()

    def get_move(self, button):
        info = button.grid_info()
        move = (int(info["row"]), int(info["column"]))  # Get move coordinates from the button's metadata
        return move

    def handle_move(self, button):
        move = self.get_move(button)
        i, j = move
        self.play(i, j)

    def initialize_tk_frame(self, root):
        """
            Initializes Tk Frame for the game.
        :return:
        """
        frame = tk.Frame(root)
        frame.grid()

        self.blocks = [[None for _ in range(self.board.height)] for _ in range(self.board.width)]

        for i in range(self.board.width):
            for j in range(self.board.height):
                self.blocks[i][j] = tk.Button(frame, height=3, width=3, text="", bg=BLOCK_DEFAULT_COLOR,
                                              command=lambda i=i, j=j: self.handle_move(self.blocks[i][j]))
                self.blocks[i][j].grid(row=i, column=j)

        self.reset_button = tk.Button(text="Reset", command=self.board.reset())
        self.reset_button.grid(row=5)

        return frame

    def switch_players(self):
        if self.current_player == self.player_one:
            self.current_player = self.player_two
            self.other_player = self.player_one
        else:
            self.current_player = self.player_one
            self.other_player = self.player_two

    def end(self):
        pass

    def is_over(self):
        return self.board.is_over()

    def reset(self):
        """
            Resets the game.
        :return:
        """
        self.board.reset()

    def get_current_player(self):
        return self.current_player

    def get_board(self):
        return self.board
