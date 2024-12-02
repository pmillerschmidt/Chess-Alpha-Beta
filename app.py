from flask import Flask, request, jsonify
from flask_cors import CORS
import chess
import chess.polyglot
from scout_agent import ScoutAgent
import PSE

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Global game state
game_board = chess.Board()
scout_agent = ScoutAgent(color=chess.BLACK, depth=4, ob='gm2001.bin')


@app.route('/new-game', methods=['GET'])
def new_game():
    global game_board
    game_board = chess.Board()
    return jsonify({"board": game_board.fen()})


@app.route('/make-move', methods=['POST'])
def make_move():
    global game_board
    data = request.json

    # Validate and make human player's move
    try:
        move = chess.Move.from_uci(data['move'])

        # Explicit move validation
        if move in game_board.legal_moves:
            # Push move on the actual game board
            game_board.push(move)

            return jsonify({
                "board": game_board.fen(),
                "move": data['move'],
                "game_over": game_board.is_game_over(),
                "result": game_board.result() if game_board.is_game_over() else None
            })
        else:
            return jsonify({"error": "Illegal move", "board": game_board.fen()}), 400

    except Exception as e:
        return jsonify({"error": str(e), "board": game_board.fen()}), 400


@app.route('/bot-move', methods=['GET'])
def bot_move():
    global game_board

    # Only make bot move if game is not over
    if not game_board.is_game_over():
        scout_agent.play(game_board)

    return jsonify({
        "board": game_board.fen(),
        "game_over": game_board.is_game_over(),
        "result": game_board.result() if game_board.is_game_over() else None
    })


@app.route('/legal-moves', methods=['GET'])
def get_legal_moves():
    global game_board
    legal_moves = [move.uci() for move in game_board.legal_moves]
    return jsonify({"legal_moves": legal_moves})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)