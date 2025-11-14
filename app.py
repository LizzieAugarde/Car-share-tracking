########## CAR SHARING APP SCRIPT ##########

import streamlit as st
import sqlite3
import pandas as pd
from datetime import date


### Prep 
# connect to the database
conn = sqlite3.connect('car_log.db', check_same_thread = False)
c = conn.cursor()

st.title("🚗 Car Sharing")


# set up tabs 
tab = st.sidebar.radio("Go to", ["Dashboard", "Log journey", "Log fuel"])


# get users for dropdown
def get_users():
    c.execute("SELECT id, name FROM users")
    return c.fetchall()


### Log a journey tab
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


### Log fuel fill up tab
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


### Dashboard tab 
elif tab == "Dashboard":
    # load data
    journeys = pd.read_sql("SELECT * FROM journeys", conn)
    fuel_logs = pd.read_sql("SELECT * FROM fuel_logs", conn)
    users = pd.read_sql("SELECT * FROM users", conn)

            
    #adding names rather than user IDs
    journeys = journeys.merge(users[['id', 'name']], left_on='user_id', right_on='id')
    journeys.drop(columns=['user_id'], inplace = True)

    fuel_logs = fuel_logs.merge(users[['id', 'name']], left_on='user_id', right_on='id')
    fuel_logs.drop(columns=['user_id'], inplace = True)  
            
            
    #renaming columns in the display tables 
    journeys.rename(columns={
        'name': 'Driver',
        'date': 'Date',
        'description': 'Purpose',
        'mileage': 'Miles driven'
    }, inplace=True)

    journeys['Date'] = pd.to_datetime(journeys['Date']).dt.strftime('%d/%m/%Y')
            
    fuel_logs.rename(columns={
        'name': 'Driver',
        'date': 'Date',
        'litres': 'Litres added',
        'cost': 'Cost'
    }, inplace=True)

    fuel_logs['Date'] = pd.to_datetime(fuel_logs['Date']).dt.strftime('%d/%m/%Y')
      
            
    #adding miles paid for to fuel logs table 
    if not fuel_logs.empty:
        fuel_logs['Miles paid for'] = fuel_logs['Litres added'] * (33/4.54609)
        

    #running statistics/balances
    if not journeys.empty:
        journeys_summary = journeys.groupby('Driver')['Miles driven'].sum().reset_index()
        journeys_summary.rename(columns={'Miles driven': 'Total miles driven'}, inplace=True)

    else:
        st.write("No journeys logged")

    if not fuel_logs.empty:
        miles_paid_summary = fuel_logs.groupby('Driver')['Miles paid for'].sum().reset_index()
        miles_paid_summary.rename(columns={'Miles paid for': 'Total miles paid for'}, inplace=True)

    else:
        st.write("No fill ups logged")

    if not fuel_logs.empty and not journeys.empty:
        comparison = journeys_summary.merge(miles_paid_summary, on = 'Driver', how = 'outer')
        comparison['Total miles paid for'] = comparison['Total miles paid for'].fillna(0)
        comparison['Total miles driven'] = comparison['Total miles driven'].fillna(0)
        comparison['Difference'] = comparison['Total miles paid for'] - comparison['Total miles driven']
        
        cols_per_row = 2

        for i in range(0, len(comparison), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, (_, row) in enumerate(comparison.iloc[i:i+cols_per_row].iterrows()):
                driver = row['Driver']
                diff = row['Difference']

                if diff > 0:
                    bg_color = "#d4edda"  
                    text_color = "#155724"
                    status = "Paid more than driven"
                elif diff < 0:
                    bg_color = "#f8d7da"  
                    text_color = "#721c24"
                    status = "Driven more than paid for"
                else:
                    bg_color = "#e2e3e5"  
                    text_color = "#383d41"
                    status = "Balanced"

                cols[j].markdown(
                    f"""
                    <div style="
                        background-color:{bg_color};
                        color:{text_color};
                        padding:15px;
                        border-radius:10px;
                        margin-bottom:10px;
                        font-size:18px;
                        font-weight:bold;
                        text-align:center;
                        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
                    ">
                        {driver}<br>
                        {status}<br>
                        ({abs(diff):.1f} miles)
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    #tables 
    if not fuel_logs.empty and not journeys.empty:
        st.subheader("Running totals")
        st.dataframe(comparison, hide_index=True)

    if not journeys.empty:
        st.subheader("Journeys")
        st.dataframe(journeys.drop(columns=['id_x', 'id_y'], errors='ignore'), hide_index=True)

    if not fuel_logs.empty:
        st.subheader("Fuel")
        st.dataframe(fuel_logs.drop(columns=['id_x', 'id_y'], errors='ignore'), hide_index=True)
        st.write(" ")
        st.write("Miles paid for is based on 33MPG and a conversion of 1 gallon to 4.5 litres, so each litre pays for 7.3 miles of driving.")
        

    #button to clear all the data from the SQLite database
    tables_to_clear = ["journeys", "fuel_logs"]
    def clear_data():
        for table in tables_to_clear:
            c.execute(f"DELETE FROM {table};")
        conn.commit()
        conn.close()

    if not fuel_logs.empty and not journeys.empty:
        if st.button("Clear all data"):
            clear_data()
            st.success("All data cleared")
            st.rerun()


