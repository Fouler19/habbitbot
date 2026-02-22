import sqlite3

conn = sqlite3.connect("habits.db", check_same_thread=False)
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS habits(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    freq TEXT,
    streak INTEGER DEFAULT 0
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS log(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id INTEGER,
    date TEXT
)
''')

conn.commit()

def add_habit(user_id, name, freq):
    cur.execute("INSERT INTO habits (user_id, name, freq) VALUES (?,?,?)", (user_id, name, freq))
    conn.commit()

def get_habits(user_id):
    cur.execute("SELECT id, name, freq, streak FROM habits WHERE user_id=?", (user_id,))
    return cur.fetchall()

def log_habit(habit_id, date):
    cur.execute("INSERT INTO log (habit_id, date) VALUES (?,?)", (habit_id, date))
    cur.execute("UPDATE habits SET streak = streak+1 WHERE id=?", (habit_id,))
    conn.commit()
