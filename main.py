import contextlib
import argparse
from random_agent import RandomAgent
from greedy_agent import GreedyAgent
from minimax_agent import MinimaxAgent
from scout_agent import ScoutAgent
from driver import Driver
with contextlib.redirect_stdout(None):
    import chess
    import chess.polyglot

def read_args():
    """
    Process command line arguments
    """
    parser = argparse.ArgumentParser(description = "Process arguments for Blotto")
    parser.add_argument('--games', type = int, required = True)
    parser.add_argument('--viz', action = 'store_true', default = False)
    args = parser.parse_args()

    num_games = args.games
    visualize = args.viz
    return (num_games, visualize)

def main():
    """
    Driver function for main program execution
    """
    num_games, visualize = read_args()

    driver = Driver()
    P1 = ScoutAgent(chess.WHITE, 3, "gm2001.bin")
    P2 = GreedyAgent(chess.BLACK, "gm2001.bin")

    if num_games == 1: print(f"Playing {1} game...")
    else: print(f"Playing {num_games} games...")
    result = driver.compare_policies(P1, P2, num_games, visualize)
    print(result)
    
if __name__ == "__main__":
    main()
    