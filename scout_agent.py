import chess

class ScoutAgent():
    
    def __init__(self, color, depth):
        self.color = color
        self.depth = depth

    def order_moves(self, board, legal_moves):
        """
        Function to order the legal moves from best to worst according to material strength
        """
        result = []
        for move in legal_moves:
            board.push(move)
            score = self.material_balance(board)
            result.append((move, score))
            board.pop()
        
        result.sort(key = lambda x: x[1])
        return result