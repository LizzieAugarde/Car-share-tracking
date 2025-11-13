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
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Driver INTEGER,
        Date TEXT,
        Description TEXT,
        Mileage REAL,
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

# users
c.execute("INSERT INTO users (name) VALUES ('Lizzie & Callum')")
c.execute("INSERT INTO users (name) VALUES ('Ruth')")

conn.commit()
conn.close()