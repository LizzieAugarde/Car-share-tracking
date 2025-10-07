import streamlit as st
import sqlite3
import pandas as pd
from datetime import date


# connect to the database
conn = sqlite3.connect('car_log.db', check_same_thread = False)
c = conn.cursor()

st.title("🚗 Car Sharing Log")


# tabs 
tab = st.sidebar.radio("Go to", ["Log journey", "Log fuel", "Dashboard"])


# helper function - get users 
def get_users():
    c.execute("SELECT id, name FROM users")
    return c.fetchall()


# log a journey
if tab == "Log journey":
    st.header("Log a journey")
    users = get_users()
    user_dict = {name: uid for uid, name in users}
    user_input = st.selectbox("Driver", list(user_dict.keys()))
    date_input = st.date_input("Date", date.today())
    desc_input = st.text_input("Description")
    mileage_input = st.number_input("Miles driven", min_value = 0.0)

    if st.button("Submit journey"):
        c.execute("INSERT INTO journeys (user_id, date, description, mileage) VALUES (?,?,?,?)",
                (user_dict[user_input], str(date_input), desc_input, mileage_input))
        conn.commit() 
        st.success("Journey logged")

# log fuel fill up 
elif tab == "Log fuel":
    st.header("Log a fuel fill-up")
    users = get_users()
    user_dict = {name: uid for uid, name in users}
    user_input = st.selectbox("Driver", list(user_dict.keys()))
    date_input = st.date_input("Date", date.today())
    litres = st.number_input("Litres", min_value = 0.0)
    cost = st.number_input("Cost (£)", min_value = 0.0)

    if st.button("Submit fuel fill up"):
        c.execute("INSERT INTO fuel_logs (user_id, date, litres, cost) VALUES (?,?,?,?)", 
                (user_dict[user_input], str(date_input), litres, cost))
        conn.commit()
        st.success("Fill up logged")


# dashboard 
elif tab == "Dashboard":
    st.header("Dashboard")

    journeys = pd.read_sql("SELECT * FROM journeys", conn)
    fuel_logs = pd.read_sql("SELECT * FROM fuel_logs", conn)
    users = pd.read_sql("SELECT * FROM users", conn)

    if not journeys.empty:
        journeys['distance'] = journeys['mileage']
        summary = journeys.groupby('user_id')['distance'].sum().reset_index()
        summary = summary.merge(users, left_on='user_id', right_on='id')
        st.subheader("Total Distance per User")
        st.bar_chart(summary.set_index('name')['distance'])

    if not fuel_logs.empty:
        fuel_logs['efficiency'] = fuel_logs['mileage'] / fuel_logs['litres']
        st.subheader("Fuel Efficiency Over Time")
        st.line_chart(fuel_logs[['date', 'efficiency']].set_index('date'))

    st.subheader("Raw Data")
    st.write("Journeys", journeys)
    st.write("Fuel Logs", fuel_logs)

