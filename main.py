import chess
import chess.polyglot
from chessboard import display
from time import sleep
from random_agent import RandomAgent
from greedy_agent import GreedyAgent
from minimax_agent import MinimaxAgent


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
    fen = 'rnbqkb1r/ppp1pppp/5n2/3p4/3P4/5NP1/PPP1PP1P/RNBQKB1R b KQkq - 0 3'
    fen2 = 'rnbqkb1r/ppp1ppp1/5n2/3p3p/3P4/5NP1/PPP1PP1P/RNBQKB1R w KQkq - 0 4'
    board = chess.Board()
    # Initialization
    game_board = display.start()
    # display.update(fen, game_board)

    while not board.is_game_over() and not display.check_for_quit(): 
        if board.turn == P1.color:
            P1.play(board)
        else:
            P2.play(board)
        # update the display
        display.update(board.fen(), game_board)

    display.update(board.fen(), game_board)
    sleep(5)
    display.terminate()
    result = board.outcome()
    return result

def main():
    """
    Driver function for main program execution
    """

    P1 = MinimaxAgent(chess.WHITE, 4, "gm2001.bin")
    P2 = GreedyAgent(chess.BLACK)
    result = compare_policies(P1, P2, 1)
    print(result)
    
    
    
if __name__ == "__main__":
    main()
    