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
    parser.add_argument('--P1', type = str, required = True, choices = ["greedy", "random", "minimax", "scout"])
    parser.add_argument('--P2', type = str, required = True, choices = ["greedy", "random", "minimax", "scout"])
    parser.add_argument('--games', type = int, required = True)
    parser.add_argument('--viz', action = 'store_true', default = False)
    args = parser.parse_args()

    player1 = args.P1
    player2 = args.P2
    num_games = args.games
    visualize = args.viz
    return (player1, player2, num_games, visualize)

def assign_player(player_color, player_type):
    if player_type == "greedy":
        return GreedyAgent(player_color, "gm2001.bin")
    if player_type == "random":
        return RandomAgent(player_color, "gm2001.bin")
    if player_type == "minimax":
        return MinimaxAgent(player_color, 3, "gm2001.bin")
    if player_type == "scout":
        return ScoutAgent(player_color, 3, "gm2001.bin")

def main():
    """
    Driver function for main program execution
    """
    player1, player2, num_games, visualize = read_args()

    driver = Driver()
    P1 = assign_player(chess.WHITE, player1)
    P2 = assign_player(chess.BLACK, player2)

    if num_games == 1: print(f"Playing {1} game...")
    else: print(f"Playing {num_games} games...")
    result = driver.compare_policies(P1, P2, num_games, visualize)
    print(result)
    
if __name__ == "__main__":
    main()
    