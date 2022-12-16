import chess
import time
import random
import math
from copy import deepcopy

class Node:
    def __init__(self, board, score = 0, visits = 0, root = False):
        self.board = board
        self.score = score
        self.visits = visits
        self.root = root

class mctsAgent():
    def __init__(self, color, time):
        self.color = color
        self.cpu_time = time

    def reward(self, board):
        if board.is_checkmate():
            reward = 500 if board.turn == chess.BLACK else -500
        elif board.is_stalemate() or board.is_insufficient_material():
            reward = 0
        
        return reward

    def rollout(self, node):
        """
        Function to randomly roll through game states to a terminal position
        """
        board = node.board
        while True:
            if board.is_game_over():
                return self.reward(board)
            legal_moves = list(board.legal_moves)
            move = random.choice(legal_moves)
            board.push(move)

    def choose_node(self, node, tree):
        """
        Function to choose which node to traverse to; random if unvisited, UCB otherwise
        """
        max_UCB = float('-inf')
        legal_moves = list(node.board.legal_moves)

        for move in legal_moves:
            node.board.push(move)
            new_board = deepcopy(node.board)
            node.board.pop()
            if tree[new_board.fen()].visits == 0:
                return tree[new_board.fen()]

        for move in legal_moves:
            node.board.push(move)
            new_board = deepcopy(node.board)
            node.board.pop()
            exploitation = tree[new_board.fen()].score / tree[new_board.fen()].visits
            if node.board.turn == chess.WHITE:
                UCB = exploitation + (2 * (math.sqrt((math.log(node.visits)) / tree[new_board.fen()].visits)))
                if UCB > max_UCB:
                    max_UCB = UCB
                    best_move = new_board

            else:
                exploitation *= -1
                UCB = exploitation + (2 * (math.sqrt((math.log(node.visits)) / tree[new_board.fen()].visits)))
                if UCB > max_UCB:
                    max_UCB = UCB
                    best_move = new_board

        return tree[best_move.fen()]
             
    def recurse(self, node, tree):
        """
        Function to recurse through the game tree, expanding when necessary
        """
        if node.board.is_game_over():
            node.visits += 1
            return self.reward(node.board)
        if not node.visits and not node.root:
            reward = self.rollout(node)
            node.visits += 1
            node.score += reward
            return reward
        else:
            if node.visits == 1:
                legal_moves = list(node.board.legal_moves)
                for move in legal_moves:
                    node.board.push(move)
                    new_board = deepcopy(node.board)
                    node.board.pop()
                    new_node = Node(board = new_board)
                    tree[new_board.fen()] = new_node
            
            new_node = self.choose_node(node, tree)
            reward = self.recurse(new_node, tree)
            node.visits += 1
            node.score += reward
            return reward

    def find_best_move(self, root, tree):
        """
        Find the best move to take from a given position
        """
        best_move, max_visits = None, float('-inf')
        legal_moves = list(root.board.legal_moves)
        for move in legal_moves:
            root.board.push(move)
            new_board = deepcopy(root.board)
            root.board.pop()
            visits = tree[new_board.fen()].visits
            if visits > max_visits:
                max_visits = visits
                best_move = move
        return best_move

    def play(self, board):
        """
        Driver function for MCTS
        """
        start = time.time()

        game_tree = {}
        root = Node(board = board, root = True)
        game_tree[board.fen()] = root

        legal_moves = list(board.legal_moves)
        for move in legal_moves:
            root.board.push(move)
            child = Node(board = root.board)
            game_tree[root.board.fen()] = child
            root.board.pop()

        while (time.time() - start) < self.cpu_time:
            curr = root
            self.recurse(curr, game_tree)

        move = self.find_best_move(root, game_tree)
        board.push(move)
