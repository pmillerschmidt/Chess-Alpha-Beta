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

    return (white_wins, draws, black_wins)  

def play_game(P1, P2):
    board = chess.Board()
    while not board.is_game_over(): 
        print(board)
        if board.turn == P1.color:
            P1.play(board)
        else:
            P2.play(board)
    
    result = board.outcome()
    return result

def main():
    P1 = MinimaxAgent(chess.WHITE, 3)
    P2 = RandomAgent(chess.BLACK)
    result = compare_policies(P1, P2, 1)
    print(result)
    
if __name__ == "__main__":
    main()