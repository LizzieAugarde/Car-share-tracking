########## DASHBOARD PAGE ##########

import streamlit as st
import sqlite3
import pandas as pd


### Prep 
# connect to the database
conn = sqlite3.connect('car_log.db', check_same_thread = False)
c = conn.cursor()

st.title("🚗 Car Sharing")
st.header("Dashboard")


# navigation sidebar 
if st.button("Menu"):
    st.session_state.show_sidebar = True 

if st.session_state.show_sidebar:
    with st.sidebar:
        tabs = ["Dashboard", "Log a journey", "Log fuel fill up"]
        choice = st.radio(" ", tabs)
        st.session_state.selected_tab = choice
        st.session_state.show_sidebar = False


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

        
fuel_logs.rename(columns={
    'name': 'Driver',
    'date': 'Date',
    'litres': 'Litres added',
    'cost': 'Cost'
}, inplace=True)

        
#adding miles paid for to fuel logs table 
if not fuel_logs.empty:
    fuel_logs['Miles paid for'] = fuel_logs['Litres added'] * (33/4.54609)
        

#running statistics 
if not journeys.empty:
    journeys_summary = journeys.groupby('Driver')['Miles driven'].sum().reset_index()
    journeys_summary.rename(columns={'Miles driven': 'Total miles driven'}, inplace=True)

if not fuel_logs.empty:
    miles_paid_summary = fuel_logs.groupby('Driver')['Miles paid for'].sum().reset_index()
    miles_paid_summary.rename(columns={'Miles paid for': 'Total miles paid for'}, inplace=True)

comparison = journeys_summary.merge(miles_paid_summary, on = 'Driver', how = 'outer')
comparison['Total miles paid for'] = comparison['Total miles paid for'].fillna(0)
comparison['Total miles driven'] = comparison['Total miles driven'].fillna(0)
comparison['Difference'] = comparison['Total miles paid for'] - comparison['Total miles driven']

st.subheader("Balances")
        
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
            extra_info = ""
        elif diff < 0:
            bg_color = "#f8d7da"  
            text_color = "#721c24"
            status = "Driven more than paid for"
            amount_owed = abs(diff) * (135.33/100) ####### CHANGE WEEKLY 
            extra_info = f"<br><span style='font-size:16px;'>Amount to pay: £{amount_owed:.2f}</span>"
        else:
            bg_color = "#e2e3e5"  
            text_color = "#383d41"
            status = "Balanced"
            extra_info = ""

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
                ({abs(diff):.1f} miles)<br>
                {extra_info}
            </div>
            """,
            unsafe_allow_html=True
        )


#tables 
st.subheader("Running totals")
st.dataframe(comparison, hide_index=True)

st.subheader("Journeys")
st.dataframe(journeys.drop(columns=['id_x', 'id_y'], errors='ignore'), hide_index=True)

st.subheader("Fuel")
st.dataframe(fuel_logs.drop(columns=['id_x', 'id_y'], errors='ignore'), hide_index=True)
st.write("Miles paid for is based on 33MPG and a conversion of 1 gallon to 4.5 litres, so each litre pays for 7.3 miles of driving.")
st.write("Balance to pay to settle up is based on the current UK average unleaded price per litre, updated weekly using RAC data:")
st.write("https://www.rac.co.uk/drive/advice/fuel-watch/#what-are-the-latest-uk-petrol-prices-and-diesel-prices")
