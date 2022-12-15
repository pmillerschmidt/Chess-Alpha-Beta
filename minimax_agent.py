import chess
import random

class MinimaxAgent():

    def __init__(self, color, depth_limit):
        self.color = color
        self.depth_limit = depth_limit

    # what material is gained from this move
    # function from StackOverflow 
    def material_gained(self, board, move):
        if board.is_capture(move):
            if board.is_en_passant(move):
                return chess.PAWN
            else:
                return board.piece_at(move.to_square).piece_type
        return 0
    
    # what is the material balance
    # from StackOverflow
    def material_balance(self, board):
        white = board.occupied_co[chess.WHITE]
        black = board.occupied_co[chess.BLACK]
        return (
            chess.popcount(white & board.pawns) - chess.popcount(black & board.pawns) +
            3 * (chess.popcount(white & board.knights) - chess.popcount(black & board.knights)) +
            3 * (chess.popcount(white & board.bishops) - chess.popcount(black & board.bishops)) +
            5 * (chess.popcount(white & board.rooks) - chess.popcount(black & board.rooks)) +
            9 * (chess.popcount(white & board.queens) - chess.popcount(black & board.queens)))
    
    # heuristic function 
    def heuristic(self, board, player):
        # if the game ends in checkmate, return very high evaluation
        if board.is_checkmate():
            reward = 500 if player == chess.WHITE else -500
        elif board.is_stalemate() or board.is_insufficient_material():
            reward = 0
        else:
            reward = self.material_balance(board)
        return reward

    
    def minimax(self, board, player, depth, depth_limit):
        # if depth is 0, return the evaluation
        if depth == 0:
            return self.heuristic(board, player)

        # if its white's turn
        if player==chess.WHITE:
            evaluations = []
            for move in board.legal_moves:
                board.push(move)
                evaluations.append((move, self.minimax(board, chess.BLACK, depth - 1, depth_limit)))
                board.pop()
            return max(evaluations, key = lambda x: x[1])
        # if its black's turn
        else:
            evaluations = []
            for move in board.legal_moves:
                board.push(move)
                evaluations.append((move, self.minimax(board, chess.WHITE, depth - 1, depth_limit)))
                board.pop()
            return min(evaluations, key = lambda x: x[1])

        
    def play(self, board):
        move = self.minimax(board, self.color, self.depth_limit, self.depth_limit)[0]
        board.push(move)
        



