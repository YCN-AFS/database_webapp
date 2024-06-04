import sqlite3


conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute("SELECT * FROM players")
players = c.fetchall()
for player in players:
    print(player)
print("--"*40)
c.execute("SELECT * FROM player_sessions")
players = c.fetchall()
for player in players:
    print(player)


print("--"*40)
c.execute("SELECT * FROM player_settings ")
players = c.fetchall()
for player in players:
    print(player)

print("--"*40)
c.execute("SELECT * FROM player_profiles")
players = c.fetchall()
for player in players:
    print(player)






conn.close()