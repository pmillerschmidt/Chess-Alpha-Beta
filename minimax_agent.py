import random
import chess
import chess.polyglot
import PSE


class MinimaxAgent():
    def __init__(self, color, depth, ob):
        self.color = color
        self.depth = depth
        self.opening_book = chess.polyglot.open_reader(ob)
        self.tt = {}

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

    def material_count(self, board):
        """
        Function that calculates the material count of the board 
        """
        count = 0
        pieces = [(1, chess.PAWN), (3.1, chess.KNIGHT),
                  (3.2, chess.BISHOP), (4.5, chess.ROOK), (9, chess.QUEEN)]

        for piece in pieces:
            count += piece[0] * len(board.pieces(piece[1], chess.WHITE))
            count += piece[0] * len(board.pieces(piece[1], chess.BLACK))

        return count

    def material_balance(self, board):
        """
        Function that calculates the material balance of the board (white pieces - black pieces)
        """
        w_balance, b_balance = 0, 0
        pieces = [(1, chess.PAWN), (3.1, chess.KNIGHT),
                  (3.2, chess.BISHOP), (4.5, chess.ROOK), (9, chess.QUEEN)]

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
            evaluation = evaluation + PSE.W_PAWN[piece] if player == chess.WHITE else evaluation - PSE.B_PAWN[piece]
        for piece in board.pieces(chess.KNIGHT, player):
            evaluation = evaluation + PSE.W_KNIGHT[piece] if player == chess.WHITE else evaluation - PSE.B_KNIGHT[piece]
        for piece in board.pieces(chess.BISHOP, player):
            evaluation = evaluation + PSE.W_BISHOP[piece] if player == chess.WHITE else evaluation - PSE.B_BISHOP[piece]
        for piece in board.pieces(chess.QUEEN, player):
            evaluation = evaluation + PSE.W_QUEEN[piece] if player == chess.WHITE else evaluation - PSE.B_QUEEN[piece]
        for piece in board.pieces(chess.KING, player):
            evaluation = evaluation + PSE.W_KING[piece] if player == chess.WHITE else evaluation - PSE.B_KING[piece]
        # normalize 
        return evaluation / 1000
    
    # attacked heuristic, sees if the position is being attacked
    # def attacked(self, board, player):
    #     color = 1 if player == chess.WHITE else -1

    #     if board.is_check():
    #         return color * 2


    def heuristic(self, board, player):
        """
        Heuristic function to determine the value of a given board position
        """
        # coefficients for material balance, piece-square evaluation
        mbc = 1
        psec = 6
        
        if board.is_checkmate():
            reward = 500 if player == chess.BLACK else -500
        elif board.is_stalemate() or board.is_insufficient_material() or board.is_fivefold_repetition():
            reward = 0
        else:
            reward = mbc * self.material_balance(board) + psec * self.piece_square_evaluation(board, player)

        return reward
    
  
    # endgame heuristic - when one side is very winning
    # see if the position is attacking/defending (checks)
    # see how mobile the king is 
    def endgame_heuristic(self, board, player):
        """
        Heuristic function to determine the value of a given board position
        """
        # coefficients for material balance, piece-square evaluation
        mbc = 1
        psec = 6
        
        if board.is_checkmate():
            reward = 500 if player == chess.BLACK else -500
        elif board.is_stalemate() or board.is_insufficient_material() or board.is_fivefold_repetition():
            reward = 0
        else:
            reward = mbc * self.material_balance(board) + psec * self.piece_square_evaluation(board, player)

        return reward

    def minimax(self, board, player, depth, alpha, beta):
        """
        Minimax algorithm with alpha-beta pruning
        """

        # if its in the transposition table, return it 
        if board.fen() in self.tt:
            return self.tt[board.fen()]

        if depth == 0 or board.is_game_over():
            if board.fen() not in self.tt:
                self.tt[board.fen()] = (None, self.heuristic(board, player))

            return self.tt[board.fen()]

        legal_moves = list(board.legal_moves)
        random.shuffle(legal_moves)

        if player == chess.WHITE:
            best_score, best_move = alpha, None
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

            self.tt[board.fen()] = (best_move, best_score)
            return (best_move, best_score)

        else:
            best_score, best_move = beta, None
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

            self.tt[board.fen()] = (best_move, best_score)
            return (best_move, best_score)

    def play(self, board):
        """
        Driver function to determine and make the best move
        """
        # play book moves until there are none
        if self.opening_book.get(board) != None:
            move = self.opening_book.weighted_choice(board).move
        
        # if we are in the endgame, up the depth
        elif self.material_count(board) < 15:
            move = self.minimax(board, self.color, self.depth + 3, float('-inf'), float('inf'))[0]

        else: 
            move = self.minimax(board, self.color, self.depth, float('-inf'), float('inf'))[0]
        
        board.push(move)
