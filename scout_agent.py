import chess

class ScoutAgent():
    
    def __init__(self, color, depth):
        self.color = color
        self.depth = depth

    def order_moves(self, board):
        """
        Function to order the legal moves from best to worst according to material strength
        """
        result = []
        legal_moves = list(board.legal_moves)
        for move in legal_moves:
            board.push(move)
            score = self.material_balance(board)
            result.append((move, score))
            board.pop()
        
        result.sort(key = lambda x: x[1])
        return result
    
    def material_balance(self, board):
        """
        Function that calculates the material balance of the board (white pieces - black pieces)
        """
        w_balance, b_balance = 0, 0
        pieces = [(1, chess.PAWN), (3.2, chess.KNIGHT),
                  (3.3, chess.BISHOP), (5, chess.ROOK), (9, chess.QUEEN)]

        for piece in pieces:
            w_balance += piece[0] * len(board.pieces(piece[1], chess.WHITE))
            b_balance += piece[0] * len(board.pieces(piece[1], chess.BLACK))

        balance = w_balance - b_balance
        return balance

    def heuristic(self, board, player):
        """
        Heuristic function to determine the value of a given board position
        """

        if board.is_checkmate():
            reward = 500 if player == chess.BLACK else -500
        elif board.is_stalemate() or board.is_insufficient_material():
            reward = 0
        else:
            reward = self.material_balance(board)
        return reward

    