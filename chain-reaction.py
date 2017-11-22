from game import Game, Player
from player_ai import AIPlay
import pickle

if __name__ == "__main__":

    player_one = Player("red")
    player_two = Player("green")

    game = Game(player_one, player_two)
    win_stats = {'red': 0, 'green': 0}

    # mode = 0 - learning mode
    # mode = 1 - testing mode
    mode = 1
    training = None
    # use previous training in the testing mode
    if mode == 1:
        with open('training.pickle', 'rb') as handle:
            training = pickle.load(handle)
    ai = AIPlay(game, training)

    for _ in range(10000):
        while True:
            print game.board.board
            print game.board.distribution
            if game.is_over():
                _, winner = game.get_board().winner()
                win_stats[winner] = win_stats[winner] + 1
                game.reset()
                break
            if game.get_current_player() == player_one:
                if mode == 0:
                    i, j = ai.get_random_move(player_one)
                if mode == 1:
                    i = raw_input()
                    j = raw_input()
            else:
                i, j = ai.get_ai_move(player_two)

            game.play(int(i), int(j))

    # If in training mode, dump all the training in a file
    if mode == 0:
        with open('training.pickle', 'wb') as handle:
            pickle.dump(ai.value_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print(win_stats)
