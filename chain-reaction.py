from game import Game, Player

if __name__ == "__main__":
    player_one = Player("red")
    player_two = Player("green")

    game = Game(player_one, player_two)

    while True:
        print game.board.board
        print game.board.distribution
        if game.is_over():
            break

        i = raw_input("enter row i")
        j = raw_input("enter col j")

        game.play(int(i), int(j))
