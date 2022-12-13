import chess
import random

class RandomAgent():

    def __init__(self, color):
        self.color = color

    def play(self, board):
        legal_moves = list(board.legal_moves)
        move = random.choice(legal_moves)
        # print(move)
        board.push(move)
