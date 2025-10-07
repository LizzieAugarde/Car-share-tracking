import sqlite3

conn = sqlite3.connect('car_log.db')
c = conn.cursor()


# create tables 
c.execute('''
CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS journeys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        description TEXT,
        mileage REAL,
        FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS fuel_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        litres REAL,
        cost REAL,
        FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

conn.commit()
conn.close()