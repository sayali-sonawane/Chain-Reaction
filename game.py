"""
    Game Module: defines the game and the rules of the game.
"""
from q_feature_board import QFeatureBoard


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

    def __init__(self, blocks, player_one, player_two, width=5, height=5):
        self.player_one = player_one
        self.player_two = player_two
        self.current_player = self.player_one
        self.other_player = self.player_two
        self.width = width
        self.height = height
        self.board = QFeatureBoard(width, height)
        self.blocks = blocks

    def play(self, i, j):
        is_legal_move = self.board.move(self.current_player.color, i, j, self.blocks)
        if not is_legal_move:
            return False

        if self.is_over():
            _, winner = self.board.winner()
            print '{} is the winner'.format(winner)
        else:
            self.switch_players()
        return True

    def get_move(self, button):
        info = button.grid_info()
        # Get move coordinates from the button's metadata
        move = (int(info["row"]), int(info["column"]))
        return move

    def handle_move(self, button, agent):
        # TODO: Handle moves based on instances of human player and Qplayers/Value Players.
        """
            This method handles moves for a Human Player
            and a Qplayer.
        :param button: Button pressed
        :param agent: Agent that plays the learned move after the human
        :return:
        """
        move = self.get_move(button)
        i, j = move
        is_legal = self.play(i, j)

        # If the human move was legal and has a GUI.
        if is_legal:
            i, j = self.handle_ai_play(agent)
            self.play(i, j)

    def handle_ai_play(self, agent):
        move = agent.get_move(self.current_player)
        return move

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
        self.reset_blocks()
        self.current_player = self.player_one
        self.other_player = self.player_two

    def reset_blocks(self):
        """
            Resets frame blocks
        """
        if self.blocks:
            for i in range(self.width):
                for j in range(self.height):
                    self.blocks[i][j].configure(text='')

    def get_current_player(self):
        return self.current_player

    def get_board(self):
        return self.board
