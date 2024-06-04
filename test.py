from flask import Flask, jsonify, render_template, request
import sqlite3

app = Flask(__name__)

# Xóa người chơi
@app.route('/players/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # Xóa người chơi từ các bảng liên quan
        c.execute("DELETE FROM player_sessions WHERE player_id = ?", (player_id,))
        c.execute("DELETE FROM player_settings WHERE player_id = ?", (player_id,))
        c.execute("DELETE FROM player_profiles WHERE player_id = ?", (player_id,))
        c.execute("DELETE FROM players WHERE player_id = ?", (player_id,))

        conn.commit()
        conn.close()
        return jsonify({'message': 'Player deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Lọc thông tin người chơi
@app.route('/players', methods=['GET'])
def get_players():
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # Lọc thông tin người chơi
        query = """
            SELECT p.player_id, p.username, p.email, pp.display_name, pp.avatar, pp.bio, ps.sound_enabled, ps.music_enabled, ps.language
            FROM players p
            LEFT JOIN player_profiles pp ON p.player_id = pp.player_id
            LEFT JOIN player_settings ps ON p.player_id = ps.player_id
        """
        c.execute(query)
        players = c.fetchall()

        conn.close()
        return jsonify([{
            'player_id': player[0],
            'username': player[1],
            'email': player[2],
            'display_name': player[3],
            'avatar': player[4],
            'bio': player[5],
            'sound_enabled': player[6],
            'music_enabled': player[7],
            'language': player[8]
        } for player in players])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Tìm kiếm người chơi theo username
@app.route('/players/search', methods=['GET'])
def search_players():
    try:
        username = request.args.get('username', '')
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # Tìm kiếm người chơi theo username
        query = """
            SELECT p.player_id, p.username, p.email, pp.display_name, pp.avatar, pp.bio, ps.sound_enabled, ps.music_enabled, ps.language
            FROM players p
            LEFT JOIN player_profiles pp ON p.player_id = pp.player_id
            LEFT JOIN player_settings ps ON p.player_id = ps.player_id
            WHERE p.username LIKE ?
        """
        c.execute(query, ('%' + username + '%',))
        players = c.fetchall()

        conn.close()
        return jsonify([{
            'player_id': player[0],
            'username': player[1],
            'email': player[2],
            'display_name': player[3],
            'avatar': player[4],
            'bio': player[5],
            'sound_enabled': player[6],
            'music_enabled': player[7],
            'language': player[8]
        } for player in players])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Lấy danh sách phiên đăng nhập của người chơi
@app.route('/players/<int:player_id>/sessions', methods=['GET'])
def get_player_sessions(player_id):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # Lấy danh sách phiên đăng nhập của người chơi
        query = """
            SELECT session_id, session_token, created_at, last_active
            FROM player_sessions
            WHERE player_id = ?
        """
        c.execute(query, (player_id,))
        sessions = c.fetchall()

        conn.close()
        return jsonify([{
            'session_id': session[0],
            'session_token': session[1],
            'created_at': session[2],
            'last_active': session[3]
        } for session in sessions])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Render template cho giao diện web
@app.route('/')
def home():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)