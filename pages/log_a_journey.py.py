########## CAR SHARING APP SCRIPT ##########

import streamlit as st
import sqlite3
from datetime import date


### Prep 
# connect to the database
conn = sqlite3.connect('car_log.db', check_same_thread = False)
c = conn.cursor()

st.title("🚗 Car Sharing")
st.header("Log a journey")


# get users for dropdown
c.execute("SELECT id, name FROM users")
users = c.fetchall()
user_dict = {name: uid for uid, name in users}


# form
user_input = st.selectbox("Driver", list(user_dict.keys()))
date_input = st.date_input("Date", date.today())
desc_input = st.text_input("Description")
mileage_input = st.number_input("Miles driven", min_value = 0.0)
    
if st.button("Submit journey"):
    c.execute("INSERT INTO journeys (user_id, date, description, mileage) VALUES (?,?,?,?)",
             (user_dict[user_input], str(date_input), desc_input, mileage_input))
    conn.commit() 
    st.success("Journey logged")
