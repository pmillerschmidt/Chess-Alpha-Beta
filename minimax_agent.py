import chess
import random

class MinimaxAgent():

    def __init__(self, color, depth):
        self.color = color
        self.depth = depth

    # what material is gained from this move
    # function from StackOverflow 
    def material_gained(self, board, move):
        if board.is_capture(move):
            if board.is_en_passant(move):
                return chess.PAWN
            else:
                return board.piece_at(move.to_square).piece_type
        return 0
    
    # edit this function to make it cleaner
    def material_balance(self, board):
        wp = len(board.pieces(chess.PAWN, chess.WHITE))
        bp = len(board.pieces(chess.PAWN, chess.BLACK))

        wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(board.pieces(chess.KNIGHT, chess.BLACK))

        wb = len(board.pieces(chess.BISHOP, chess.WHITE))
        bb = len(board.pieces(chess.BISHOP, chess.BLACK))

        wr = len(board.pieces(chess.ROOK, chess.WHITE))
        br = len(board.pieces(chess.ROOK, chess.BLACK))

        wq = len(board.pieces(chess.QUEEN, chess.WHITE))
        bq = len(board.pieces(chess.QUEEN, chess.BLACK))
        
        evaluation = (wp - bp) + 3.2 * (wn - bn) + 3.3 * (wb - bb) + 5 * (wr - br) + 9 * (wq - bq)

        return evaluation
        
    def heuristic(self, board, player):
        if board.is_checkmate():
            reward = 500 if player == chess.BLACK else -500
        elif board.is_stalemate() or board.is_insufficient_material():
            reward = 0
        else:
            reward = self.material_balance(board)
        return reward

    
    def minimax(self, board, player, depth):
        if depth == 0 or board.is_game_over():
            return (None, self.heuristic(board, player))

        if player == chess.WHITE:
            best_score, best_move = float('-inf'), None
            for move in board.legal_moves:
                board.push(move)
                score = self.minimax(board, chess.BLACK, depth - 1)

                if score[1] > best_score:
                    best_score = score[1]
                    best_move = move
                # pop the last move 
                board.pop()
            return (best_move, best_score)

        else:
            best_score, best_move = float('inf'), None
            for move in board.legal_moves:
                board.push(move)
                score = self.minimax(board, chess.WHITE, depth - 1)
                
                if score[1] < best_score:
                    best_score = score[1]
                    best_move = move
                board.pop()

            return (best_move, best_score)
            
        
    def play(self, board):
        move = self.minimax(board, self.color, self.depth)[0]
        board.push(move)
