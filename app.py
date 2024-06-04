from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g
import sqlite3
import datetime
import random
import string
from encryption import hash_password, check_password

current_time = datetime.datetime.now()



app = Flask(__name__)
# app.post()
app.static_folder = 'static'
app.secret_key = 'your_secret_key'


bio = (
    "Sống là để học hỏi, yêu thương và lan tỏa niềm vui.",
    "Mỗi ngày là một món quà quý giá, hãy trân trọng từng khoảnh khắc.",
    "Hãy luôn hướng về phía trước với một trái tim dũng cảm và một tinh thần lạc quan.",
    "Tin tưởng vào bản thân và đừng bao giờ bỏ cuộc trước ước mơ của bạn.",
    "Hãy tử tế với mọi người, dù họ là ai hay họ đến từ đâu.",
    "Sự tha thứ là chìa khóa dẫn đến hạnh phúc và bình yên.",
    "Hãy biết ơn những gì bạn đang có và luôn sẵn sàng giúp đỡ người khác.",
    "Sống một cuộc đời có ý nghĩa là sống một cuộc đời cống hiến.",
    "Hãy để lại dấu ấn tích cực trên thế giới này.",
    "Hãy luôn là chính mình và đừng ngại thể hiện bản sắc độc đáo của bạn.",
    "Sống cho hiện tại và tận hưởng từng khoảnh khắc.",
    "Hãy luôn học hỏi và phát triển bản thân.",
    "Đừng bao giờ ngừng mơ ước và theo đuổi đam mê của bạn.",
    "Hãy can đảm đối mặt với thử thách và vượt qua giới hạn của bản thân.",
    "Tin tưởng vào sức mạnh của tình yêu và sự kết nối.",
    "Hãy luôn biết ơn những người đã giúp đỡ bạn trên chặng đường.",
    "Sống một cuộc đời trọn vẹn và ý nghĩa.",
    "Để lại di sản tốt đẹp cho thế hệ sau.",
    "Làm cho thế giới trở nên tốt đẹp hơn.",
)


conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS players (
                player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) NOT NULL UNIQUE,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")

c.execute("""CREATE TABLE IF NOT EXISTS player_profiles (
                profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                display_name VARCHAR(50) NOT NULL,
                avatar VARCHAR(200),
                bio TEXT,
                FOREIGN KEY (player_id) REFERENCES players(player_id)
            )""")

c.execute("""CREATE TABLE IF NOT EXISTS player_settings (
                setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                sound_enabled BOOLEAN DEFAULT TRUE,
                music_enabled BOOLEAN DEFAULT TRUE,
                language VARCHAR(10) DEFAULT 'en',
                FOREIGN KEY (player_id) REFERENCES players(player_id)
            )""")

c.execute("""CREATE TABLE IF NOT EXISTS player_sessions (
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                session_token VARCHAR(100) NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES players(player_id)
            )""")

# conn.commit()
# conn.close()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('database.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        c = db.cursor()
        c.execute("SELECT * FROM players WHERE username=?", (username,))
        user = c.fetchone()

        #Random token
        session_token = ''.join(random.choice(string.printable) for i in range(12))

        if user and check_password(password, user[3]):
            db = get_db()
            c = db.cursor()

            c.execute("INSERT INTO player_sessions (player_id, session_token, created_at, last_active) VALUES (?, ?, ?, ?)",
             (user[0], session_token, user[4],  current_time.strftime("%H:%M:%S | %d-%m-%Y")))
            db.commit()
            
            flash('Đăng nhập thành công!', 'success')

            if user[1] == 'admin':
                return render_template('edit.html')
            return redirect(url_for('herta_kuru'))
        else:
            error = 'Tên đăng nhập hoặc mật khẩu không đúng'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        display_name = request.form['display_name']
        password = request.form['password']
        email = request.form['email']
        
        db = get_db()
        pr = get_db()
        st = get_db()

        c = db.cursor()
        d = pr.cursor()
        e = st.cursor()
        try:
            c.execute("INSERT INTO players (username, email, password, created_at) VALUES (?, ?, ?, ?)", (username, email, hash_password(password), current_time.strftime("%H:%M:%S | %d-%m-%Y")))
            d.execute("INSERT INTO player_profiles (player_id, display_name, avatar, bio) VALUES (?, ?, ?, ?)", (c.lastrowid, display_name, None, random.choice(bio)))
            e.execute("INSERT INTO player_settings (player_id, sound_enabled, music_enabled, language) VALUES (?, ?, ?, ?)", (c.lastrowid, True, True, 'en'))
            
            pr.commit()
            db.commit()
            st.commit()
            flash('Đăng ký thành công!', 'success')
            return render_template('register_success.html')
        except:
            error = False 
    return render_template('register.html', error=error)

@app.route('/herta_kuru')
def herta_kuru():
    return render_template('herta_kuru.html')

@app.route('/players/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        c.execute("DELETE FROM player_sessions WHERE player_id = ?", (player_id,))
        c.execute("DELETE FROM player_settings WHERE player_id = ?", (player_id,))
        c.execute("DELETE FROM player_profiles WHERE player_id = ?", (player_id,))
        c.execute("DELETE FROM players WHERE player_id = ?", (player_id,))

        conn.commit()
        conn.close()
        return jsonify({'message': 'Player deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/players', methods=['GET'])
def get_players():
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()


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


@app.route('/players/search', methods=['GET'])
def search_players():
    try:
        username = request.args.get('username', '')
        conn = sqlite3.connect('database.db')
        c = conn.cursor()


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


@app.route('/players/<int:player_id>/sessions', methods=['GET'])
def get_player_sessions(player_id):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
