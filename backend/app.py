from flask import Flask, request, jsonify
from logic import ConnectFour
from uuid import uuid4
from datetime import datetime, timedelta
import threading
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

games = {}
game_expiry_minutes = 30

@app.route('/start', methods=['POST'])
def start_game():
    game_id = str(uuid4())
    data = request.get_json()
    mode = data.get('mode', 'pvp')
    player1 = data.get('player1', 'Player 1')
    player2 = data.get('player2', 'Player 2')
    difficulty = data.get('difficulty', 'hard')
    game = ConnectFour(mode=mode, player1=player1, player2=player2, difficulty=difficulty)
    games[game_id] = {
        'game': game,
        'last_active': datetime.utcnow()
    }
    return jsonify({"message": "Game started", "game_id": game_id, "state": game.get_state()})


@app.route('/move', methods=['POST'])
def make_move():
    data = request.get_json()
    game_id = data.get('game_id')
    col = data.get('column')

    if not game_id or game_id not in games:
        return jsonify({"error": "Invalid or missing game_id"}), 400

    try:
        col = int(col)
        if col < 0 or col > 6:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid column. Must be integer from 0 to 6"}), 400

    session = games[game_id]
    session['last_active'] = datetime.utcnow()
    result = session['game'].make_move(col)
    return jsonify({"result": result, "state": session['game'].get_state()})


@app.route('/ai-move', methods=['POST'])
def ai_move():
    data = request.get_json()
    game_id = data.get('game_id')

    if not game_id or game_id not in games:
        return jsonify({"error": "Invalid or missing game_id"}), 400

    session = games[game_id]
    session['last_active'] = datetime.utcnow()
    result = session['game'].ai_move()
    return jsonify({"result": result, "state": session['game'].get_state()})


@app.route('/state', methods=['GET'])
def get_state():
    game_id = request.args.get('game_id')
    if not game_id or game_id not in games:
        return jsonify({"error": "Invalid or missing game_id"}), 400
    session = games[game_id]
    session['last_active'] = datetime.utcnow()
    return jsonify(session['game'].get_state())


def cleanup_games():
    while True:
        now = datetime.utcnow()
        to_delete = []
        for gid, session in games.items():
            game = session['game']
            last_active = session['last_active']
            if game.game_over or (now - last_active) > timedelta(minutes=game_expiry_minutes):
                to_delete.append(gid)
        for gid in to_delete:
            del games[gid]
        threading.Event().wait(60)


if __name__ == '__main__':
    threading.Thread(target=cleanup_games, daemon=True).start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)