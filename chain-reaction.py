from game import Game, Player
from player_ai import AIPlay
from q_value import QValueAgent
import pickle

if __name__ == "__main__":

    player_one = Player("red")
    player_two = Player("green")

    game = Game(player_one, player_two)
    win_stats = {'red': 0, 'green': 0}

    # mode = 0 - testing mode
    # mode = 1 - learning mode for Value Agent
    # mode = 2 - learning mode for Q-Value Agent
    mode = 2
    training = None
    # use previous training in the testing mode
    if mode == 0:
        with open('training.pickle', 'rb') as handle:
            training = pickle.load(handle)
    ai = AIPlay(game, training)
    q_agent = QValueAgent(game, training)

    for _ in range(100000):
        while True:
            print game.board.board
            print game.board.distribution
            if game.is_over():
                _, winner = game.get_board().winner()
                win_stats[winner] = win_stats[winner] + 1
                game.reset()
                break
            if game.get_current_player() == player_one:
                if mode == 1:
                    i, j = ai.get_random_move(player_one)
                if mode == 2:
                    i, j = q_agent.get_random_move(player_one)
                if mode == 0:
                    i = raw_input()
                    j = raw_input()
            else:
                if mode == 1:
                    i, j = ai.get_ai_move(player_two)
                if mode == 2:
                    i, j = q_agent.get_move(player_two)

            game.play(int(i), int(j))

    # If in training mode, dump all the training in a file
    if mode == 1:
        with open('training.pickle', 'wb') as handle:
            pickle.dump(ai.value_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    if mode == 2:
        with open('training_Q_values.pickle', 'wb') as handle:
            pickle.dump(q_agent.q_values, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print(win_stats)