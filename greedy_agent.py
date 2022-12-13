import chess
import random

class GreedyAgent():

    def __init__(self, color):
        self.color = color

    # what material is gained from this move
    # function from StackOverflow 
    def material_gained(self, board, move):
        if board.is_capture(move):
            if board.is_en_passant(move):
                return chess.PAWN
            else:
                return board.piece_at(move.to_square).piece_type
        return 0

    def play(self, board):
        legal_moves = list(board.legal_moves)
        max_material = 0
        best_move = None
        # go through moves, choose one with the most material gain
        for move in legal_moves:
            if self.material_gained(board, move) > max_material:
                max_material = self.material_gained(board, move)
                best_move = move

        # if no move is best
        if max_material == 0:
            best_move = random.choice(legal_moves)

        board.push(best_move)



