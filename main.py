import chess
from random_agent import RandomAgent


def main():
    board = chess.Board()
    P1 = RandomAgent()
    P2 = RandomAgent()
    game_over = False

    # while not board.is_checkmate():
    while not game_over:
        # if its checkmate
        if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material():
            game_over = True
            break

        # print(board)
        # if its whites turn 
        if board.turn == chess.WHITE:
            P1.play(board)
        else:
            P2.play(board)
    
    result = board.outcome()
    print(result)
    
    
        


if __name__ == "__main__":
    main()