"""
    Game Module: defines the game and the rules of the game.
"""
from board import Board


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

    def __init__(self, player_one, player_two):
        self.player_one = player_one
        self.player_two = player_two
        self.current_player = self.player_one
        self.other_player = self.player_two
        self.board = Board()

    def play(self, i, j):
        self.board.move(self.current_player, i, j)
        if self.is_over():
            _, winner = self.board.winner()
            print '{} is the winner'.format(winner)
        else:
            self.switch_players()

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
