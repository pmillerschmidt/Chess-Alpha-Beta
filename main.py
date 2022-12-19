import chess
import chess.polyglot
from chessboard import display
from time import sleep
from random_agent import RandomAgent
from greedy_agent import GreedyAgent
from minimax_agent import MinimaxAgent
from scout_agent import ScoutAgent

def compare_policies(P1, P2, simulations):
    """
    Function to compare the outcome of a game between different policies
    """
    white_wins = draws = black_wins = 0
    for _ in range(simulations):
        result = play_game(P1, P2)
        if result.winner == True: white_wins += 1
        elif result.winner == False: black_wins += 1
        else: draws += 1

    return (white_wins, draws, black_wins)  

def play_game(P1, P2):
    """
    Function to make turns for each respective player while the game is active
    """
    # Initialization
    game_board = display.start()
    board = chess.Board()

    # Play until game is over or has been quit
    while not board.is_game_over() and not display.check_for_quit():
        P1.play(board) if board.turn == P1.color else P2.play(board)
        display.update(board.fen(), game_board)

    # Finish up 
    display.update(board.fen(), game_board)
    result = board.outcome()
    return result

def main():
    """
    Driver function for main program execution
    """
    P1 = ScoutAgent(chess.WHITE, 3, "gm2001.bin")
    P2 = MinimaxAgent(chess.BLACK, 3, "gm2001.bin")
    result = compare_policies(P1, P2, 1)
    print(result)
    

if __name__ == "__main__":
    main()
    