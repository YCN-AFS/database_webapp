import sqlite3


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

conn.commit()
conn.close()