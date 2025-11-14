########## CAR SHARING APP SCRIPT ##########

import streamlit as st
import sqlite3
from datetime import date


### Prep 
# connect to the database
conn = sqlite3.connect('car_log.db', check_same_thread = False)
c = conn.cursor()

st.title("🚗 Car Sharing")
st.header("Log fuel fill up")


# get users for dropdown
c.execute("SELECT id, name FROM users")
users = c.fetchall()
user_dict = {name: uid for uid, name in users}


# form
user_input = st.selectbox("Driver", list(user_dict.keys()))
date_input = st.date_input("Date", date.today())
litres = st.number_input("Litres", min_value = 0.0)
cost = st.number_input("Cost (£)", min_value = 0.0)

if st.button("Submit fuel fill up"):
    c.execute("INSERT INTO fuel_logs (user_id, date, litres, cost) VALUES (?,?,?,?)", 
             (user_dict[user_input], str(date_input), litres, cost))
    conn.commit()
    st.success("Fill up logged")

