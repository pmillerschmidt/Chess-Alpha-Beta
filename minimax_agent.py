import random
import chess
import PSE


class MinimaxAgent():
    def __init__(self, color, depth):
        self.color = color
        self.depth = depth

    def material_gained(self, board, move):
        """
        Function to determine the material gained from a given move
        Citation: https://stackoverflow.com/questions/61778579/what-is-the-best-way-to-find-out-if-the-move-captured-a-piece-in-python-chess
        """
        if board.is_capture(move):
            if board.is_en_passant(move):
                return chess.PAWN
            else:
                return board.piece_at(move.to_square).piece_type
        return 0

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

    def piece_square_evaluation(self, board, player):
        """
        Function that evaluates the positional strength of a player's pieces
        """
        evaluation = 0
        # # do something different for black? Do I need to flip the board
        for piece in board.pieces(chess.PAWN, player):
            evaluation += PSE.PAWN[piece]
        for piece in board.pieces(chess.KNIGHT, player):
            evaluation += PSE.KNIGHT[piece]
        for piece in board.pieces(chess.BISHOP, player):
            evaluation += PSE.BISHOP[piece]
        for piece in board.pieces(chess.QUEEN, player):
            evaluation += PSE.QUEEN[piece]
        for piece in board.pieces(chess.KING, player):
            evaluation += PSE.KING[piece]
        # normalize to easier values
        # maybe we can change this normalization to a value between [0, 1]
        evaluation = evaluation / 100
        # print(evaluation)
        return evaluation

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

    def minimax(self, board, player, depth, alpha, beta):
        """
        Minimax algorithm with alpha-beta pruning
        """
        if depth == 0 or board.is_game_over():
            return (None, self.heuristic(board, player))

        legal_moves = list(board.legal_moves)
        random.shuffle(legal_moves)

        if player == chess.WHITE:
            best_score, best_move = float('-inf'), None
            for move in legal_moves:
                board.push(move)
                score = self.minimax(board, chess.BLACK, depth - 1, alpha, beta)

                if score[1] > best_score:
                    best_score = score[1]
                    best_move = move
                    alpha = max(alpha, best_score)

                board.pop()
                if beta <= alpha:
                    break

            return (best_move, best_score)

        else:
            best_score, best_move = float('inf'), None
            for move in legal_moves:
                board.push(move)
                score = self.minimax(board, chess.WHITE, depth - 1, alpha, beta)

                if score[1] < best_score:
                    best_score = score[1]
                    best_move = move
                    beta = min(beta, best_score)

                board.pop()
                if beta <= alpha:
                    break

            return (best_move, best_score)

    def play(self, board):
        """
        Driver function to determine and make the best move
        """
        move = self.minimax(board, self.color, self.depth, float('-inf'), float('inf'))[0]
        board.push(move)
