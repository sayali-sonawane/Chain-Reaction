import numpy as np
import random
import operator

class qFeatureAgent:
    def __init__(self, game, feature_weight, learning_rate = 0.0001, discount = 0.9):
        self.learning_rate = learning_rate
        self.discount = discount
        self.feature_weight = feature_weight if feature_weight else [4813892.250646295, -13072235.845735667, 13941787.715611592, 46137336.693618439, 63087154.110843077, 6154015.123595411, 28760997.80778924, 4901901058.0867653, 277740430.16663039]
        self.game = game
        self.board = self.game.board
        self.currentQ = 0
        self.player = None
        self.move = None
        self.diff = 0
        # self.distribution = self.game.distribution

    def get_move(self, player):
        threshold = 0.99
        rand = random.random()
        self.player = player.color
        next_moves = self.board.get_available_moves(self.player)
        if (rand < threshold):
            current_board,current_distribution = self.board.give_board_status()
            current_board_rep = self.board.get_board_rep()
            max_move = None
            max_q = -1*np.inf
            favMovesSorted = []
            favMoves = {}
            feature_weight = self.feature_weight
            for move in next_moves:

                board_after_move = self.board.get_dummy_board_after_move(move, self.player)
                q_after_move = self.calcReward(board_after_move.board, board_after_move.distribution, move, feature_weight)
                after_state_rep = self.board.get_dummy_board_after_move_rep(move, self.player)
                # board_after_move = self.board.get_dummy_board_after_move(move, player.color)
                reward_after_move = self.get_comparitive_reward(current_board_rep, after_state_rep)

                # if (max_q < q_after_move + reward_after_move):
                max_q = self.discount*(q_after_move) + reward_after_move
                favMoves[move] = max_q

            move_max = max(favMoves, key=lambda key: favMoves[key])
            choices = []
            for itm in favMoves:
                if favMoves[itm] == favMoves[move_max]:
                    choices.append(itm)

            max_move = random.choice(choices)
            max_q = favMoves[max_move]
            diff = max_q - self.currentQ
            self.diff = diff
            self.move = max_move
            board_after_move = self.board.get_dummy_board_after_move(max_move, self.player)
            self.feature_weight = self.updateWeight(feature_weight, diff, board_after_move.board, board_after_move.distribution, max_move)
            self.currentQ = max_q
            print("feature weight ..... "+str(self.feature_weight)+" Diff "+str(diff))
            return max_move
        else:
            return random.choice(next_moves)

    def dist(self, board, distribution, move):
        (i,j) = move
        height, width = distribution.shape
        count = []

        if board[i][j] < 3:
            if (j+1 < width and distribution[i][j+1] != 1.0):
                count.append(board[i][j] - 2*board[i][j+1])
            if (j-1 > -1 and distribution[i][j-1] != 1.0):
                count.append(board[i][j] - 2*board[i][j-1])
            if (i+1 < height and distribution[i+1][j] != 1.0):
                count.append(board[i][j] - 2*board[i+1][j])
            if (i-1 > -1 and distribution[i-1][j] != 1.0):
                count.append(board[i][j] - 2*board[i-1][j])
        if count:
            min_count = min(count)
            max_count = max(count)
            return min_count/3
        return 0

    def playerCount(self, board, distribution, move):
        i,j = move
        player_count = 0
        opponent_count = 0
        if (j + 1 < self.board.width):
            if distribution[i][j + 1] != 1.0:
                opponent_count += board[i][j+1]
            else:
                player_count += board[i][j+1]
        if (j - 1 > -1):
            if distribution[i][j - 1] != 1.0:
                opponent_count += board[i][j-1]
            else:
                player_count += board[i][j-1]
        if (i + 1 < self.board.height):
            if distribution[i+1][j] != 1.0:
                opponent_count += board[i+1][j]
            else:
                player_count += board[i+1][j]
        if (i - 1 > -1):
            if distribution[i-1][j] != 1.0:
                opponent_count += board[i-1][j]
            else:
                player_count += board[i-1][j]
        return player_count - opponent_count
        # return 0

    def bubbleCount(self, board, distribution):
        countOne = 0
        countTwo = 0
        countThree = 0
        oppOne = 0
        oppTwo = 0
        oppThree = 0
        for i in range(self.board.height):
            for j in range(self.board.width):
                if (distribution[i][j] == 1.0 and board[i][j] == 1):
                    countOne += 1
                if (distribution[i][j] == 1.0 and board[i][j] == 2):
                    countTwo += 1
                if (distribution[i][j] == 1.0 and board[i][j] == 3):
                    countThree += 1
                if (distribution[i][j] == 0.0 and board[i][j] == 1):
                    oppOne += 1
                if (distribution[i][j] == 0.0 and board[i][j] == 2):
                    oppTwo += 1
                if (distribution[i][j] == 0.0 and board[i][j] == 3):
                    oppThree += 1
        a = float(countOne + countTwo * 3 + countThree * 5) / float(self.board.height * self.board.width)
        b = float(oppOne + oppTwo * 3 + oppThree * 5) / float(self.board.height * self.board.width)
        f4 = 0
        if a > b:
            f4 = (a - b)*2 + 10
        if a <= b:
            f4 = (a - b)*2 - 10

        # f5 = float(oppOne + oppTwo*3 + oppThree*5)/float(self.board.height * self.board.width * 3)
        return float(countOne)/float(self.board.height * self.board.width),\
               float(countTwo)*3/float(self.board.height * self.board.width),\
               float(countThree)*5/float(self.board.height * self.board.width), f4
        # return 0,0,0,f4

    def threeAttack(self, board, distribution, move):
        i,j = move
        count = 3
        unfav_count = 0
        if board[i][j] == 3:
            if i+1 < self.board.height and distribution[i+1][j] == 0.0:
                count += board[i+1][j]

            if i-1 > -1 and distribution[i-1][j] == 0.0:
                count += board[i-1][j]

            if j+1 < self.board.width and distribution[i][j+1] == 0.0:
                count += board[i][j+1]

            if j-1 > -1 and distribution[i][j-1] == 0.0:
                count += board[i][j-1]


            # if i + 2 < self.board.height and distribution[i + 2][j] == 0.0 and board[i + 2][j] == 3:
            #     unfav_count += 1
            # if i-2 > -1 and distribution[i-2][j] == 0.0 and board[i-2][j] == 3:
            #     unfav_count += 1
            # if j+2 < self.board.width and distribution[j+2][j] == 0.0 and board[j+2][j] == 3:
            #     unfav_count += 1
            # if j-2 > -1 and distribution[j-2][j] == 0.0 and board[j-2][j] == 3:
            #     unfav_count += 1
            # if i+1
        return count/5

    # def twoNeighbor(self, board, distribution):


    # def twoStepDist(self, board, distribution, move):
    #     i,j = move
    #     height, width = distribution.shape
    #     if (j+2 < width and distribution[i][j+2] != 1.0):
    #         count = board[i][j+2] - board[i][j]
    #         if (count > max):
    #             max = count
    #     if (j-2 > -1 and distribution[i][j-2] != 1.0):
    #         count = board[i][j-2] - board[i][j]
    #         if (count > max):
    #             max = count
    #     if (i+2 < height and distribution[i+2][j] != 1.0):
    #         count = board[i+2][j] - board[i][j]
    #         if (count > max):
    #             max = count
    #     if (i-2 > -1 and distribution[i-2][j] != 1.0):
    #         count = board[i-2][j] - board[i][j]
    #         if (count > max):
    #             max = count

    def twoStepAttack(self, board, distribution, move):
        i,j = move
        count = 0
        unfav_count = 0
        if i + 2 < self.board.height and distribution[i + 2][j] == 0.0 and board[i][j] - board[i+2][j] < 0:
            count += 1
            if (board[i + 2][j] == 3):
                count -= 1
                unfav_count += 1
        if i - 2 > -1 and distribution[i - 2][j] == 0.0 and board[i][j] - board[i-2][j] < 0:
            count += 1
            if (board[i - 2][j] == 3):
                count -= 1
                unfav_count += 1
        if j + 2 < self.board.width and distribution[i][j + 2] == 0.0 and board[i][j] - board[i][j+2] < 0:
            count += 1
            if (board[i][j + 2] == 3):
                count -= 1
                unfav_count += 1
        if j - 2 > -1 and distribution[i][j - 2] == 0.0 and board[i][j] - board[i][j-2] < 0:
            count += 1
            if (board[i][j - 2] == 3):
                count -= 1
                unfav_count += 1
        if i+1 < self.board.height and j+1 < self.board.width and distribution[i + 1][j+1] == 0.0 and board[i][j] - board[i+1][j+1] < 0:
            count += 1
            if (board[i + 1][j + 1] == 3):
                count -= 1
                unfav_count += 1
        if i + 1 < self.board.height and j - 1 > -1 and distribution[i + 1][j - 1] == 0.0 and board[i][j] - board[i + 1][j - 1] < 0:
            count += 1
            if (board[i + 1][j - 1] == 3):
                count -= 1
                unfav_count+= 1
        if i - 1 > -1 and j + 1 < self.board.width and distribution[i - 1][j + 1] == 0.0 and board[i][j] - board[i - 1][j + 1] < 0:
            count += 1
            if (board[i - 1][j + 1] == 3):
                count -= 1
                unfav_count += 1
        if i - 1 > -1 and j - 1 > -1 and distribution[i - 1][j - 1] == 0.0 and board[i][j] - board[i - 1][j - 1] < 0:
            count += 1
            if (board[i - 1][j - 1] == 3):
                count -= 1
                unfav_count += 1

        return (count-unfav_count)/8

    def calcReward(self, board, distribution, move, feature_weight):
        f1 = self.dist(board, distribution, move)
        # f2,f3 = self.playerCount(board, distribution)
        f2,f3,f4,f7 = self.bubbleCount(board, distribution)
        f5 = self.threeAttack(board, distribution, move)
        f6 = self.twoStepAttack(board, distribution, move)
        f8 = self.playerCount(board, distribution, move)

        w0 = feature_weight[0]
        w1 = feature_weight[1]
        w2 = feature_weight[2]
        w3 = feature_weight[3]
        w4 = feature_weight[4]
        w5 = feature_weight[5]
        w6 = feature_weight[6]
        w7 = feature_weight[7]
        w8 = feature_weight[8]

        reward = w0 + w1*(f1) + w2*f2 + w3*(f3) + w4*f4 + w5*f5 + w6*f6 +w7*f7 + w8*f8

        return reward

    def get_comparitive_reward(self, current_rep, afterstate_rep):
        # Gives the expected immediate reward after the move
        if 'a' not in afterstate_rep and 'b' not in afterstate_rep and 'c' not in afterstate_rep:
            if self.find_score(current_rep) != 0:
                return 1000
        elif 'x' not in afterstate_rep and 'y' not in afterstate_rep and 'z' not in afterstate_rep:
            if self.find_score(current_rep) != 0:
                return -1000

        # a = self.find_score(afterstate_rep)
        # b = self.find_score(current_rep)
        #
        # if a > b:
        #     return (a - b) * 2 + 10
        # if a <= b:
        #     return (a - b) * 2 - 10
        return 0

    def find_score(self, afterstate_rep):
        rep = list(afterstate_rep)
        score = rep.count('x') + rep.count('y') * 3 + rep.count('z') * 5
        return score

    def updateWeight(self, feature_weight, diff, board, distribution, move):
        w0 = feature_weight[0]
        w1 = feature_weight[1]
        w2 = feature_weight[2]
        w3 = feature_weight[3]
        w4 = feature_weight[4]
        w5 = feature_weight[5]
        w6 = feature_weight[6]
        w7 = feature_weight[7]
        w8 = feature_weight[8]

        f1 = self.dist(board, distribution, move)
        # f2,f3 = self.playerCount(board, distribution)
        f2, f3, f4, f7 = self.bubbleCount(board, distribution)
        f5 = self.threeAttack(board, distribution, move)
        f6 = self.twoStepAttack(board, distribution, move)
        f8 = self.playerCount(board, distribution, move)

        q = w0 + w1*f1 + w2*f2 + w3*f3 + w4*f4 + w5*f5 + w6*f6 +w7*f7 + w8*f8

        w0 = w0 + self.learning_rate * diff
        w1 = w1 + self.learning_rate * diff * f1
        w2 = w2 + self.learning_rate * diff * f2
        w3 = w3 + self.learning_rate * diff * f3
        w4 = w4 + self.learning_rate * diff * f4
        w5 = w5 + self.learning_rate * diff * f5
        w6 = w6 + self.learning_rate * diff * f6
        w7 = w7 + self.learning_rate * diff * f7
        w8 = w8 + self.learning_rate * diff * f8

        updated_feature_weight = [None]*9
        updated_feature_weight[0] = w0
        updated_feature_weight[1] = w1
        updated_feature_weight[2] = w2
        updated_feature_weight[3] = w3
        updated_feature_weight[4] = w4
        updated_feature_weight[5] = w5
        updated_feature_weight[6] = w6
        updated_feature_weight[7] = w7
        updated_feature_weight[8] = w8

        return updated_feature_weight

    def update(self, player):
        after_state_rep = self.board.get_board_rep()
        board = self.board.board
        distribution = self.board.distribution
        reward = 0
        if 'a' not in after_state_rep and 'b' not in after_state_rep and 'c' not in after_state_rep:
            reward = 1000
        elif 'x' not in after_state_rep and 'y' not in after_state_rep and 'z' not in after_state_rep:
            reward = -10

        weight = self.feature_weight
        w0 = weight[0]
        w1 = weight[1]
        w2 = weight[2]
        w3 = weight[3]
        w4 = weight[4]
        w5 = weight[5]
        w6 = weight[6]
        w7 = weight[7]
        w8 = weight[8]
        w0 = w0 + self.learning_rate * reward
        w1 = w1 + self.learning_rate * reward
        w2 = w2 + self.learning_rate * reward
        w3 = w3 + self.learning_rate * reward
        w4 = w4 + self.learning_rate * reward
        w5 = w5 + self.learning_rate * reward
        w6 = w6 + self.learning_rate * reward
        w7 = w7 + self.learning_rate * reward
        w8 = w8 + self.learning_rate * reward

        updated_feature_weight = [None] * 9
        updated_feature_weight[0] = w0
        updated_feature_weight[1] = w1
        updated_feature_weight[2] = w2
        updated_feature_weight[3] = w3
        updated_feature_weight[4] = w4
        updated_feature_weight[5] = w5
        updated_feature_weight[6] = w6
        updated_feature_weight[7] = w7
        updated_feature_weight[8] = w8

        self.feature_weight = updated_feature_weight

