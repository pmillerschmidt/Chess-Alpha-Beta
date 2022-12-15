import chess
from random_agent import RandomAgent
from greedy_agent import GreedyAgent
from minimax_agent import MinimaxAgent


def compare_policies(P1, P2, simulations):
    white_wins = draws = black_wins = 0
    for i in range(simulations):
        result = play_game(P1, P2)
        if result.winner == True: white_wins += 1
        elif result.winner == False: black_wins += 1
        else: draws += 1

    # returns white wins, draws, and black wins
    return (white_wins, draws, black_wins)
    

def play_game(P1, P2):
    board = chess.Board()
    game_over = False
    # while not board.is_checkmate():
    while not game_over: 
        # if its checkmate
        if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material():
            game_over = True
            break

        # if its whites turn 
        if board.turn == P1.color:
            P1.play(board)
        else:
            P2.play(board)
    
    result = board.outcome()
    return result

def main():

    P1 = MinimaxAgent(chess.WHITE, 10)
    P2 = RandomAgent(chess.BLACK)
    result = compare_policies(P1, P2, 1)
    print(result)
    
        


if __name__ == "__main__":
    main()