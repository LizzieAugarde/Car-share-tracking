import psycopg2
import streamlit as st

def init_db():
        conn = psycopg2.connect(
                host=st.secrets["db"]["host"],
                database=st.secrets["db"]["name"],
                user=st.secrets["db"]["user"],
                password=st.secrets["db"]["password"],
                port=st.secrets["db"]["port"]
        )

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
                name TEXT,
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

# users
        c.execute("INSERT INTO users (name) VALUES ('Lizzie & Callum')")
        c.execute("INSERT INTO users (name) VALUES ('Ruth')")

        conn.commit()
        conn.close()