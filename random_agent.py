import chess
import random

class RandomAgent():

        

    def play(self, board):
        legal_moves = list(board.legal_moves)
        move = chess.Move.from_uci(str(random.choice(legal_moves)))
        # print(move)
        board.push(move)
