import pandas as pd
import sqlite3
import streamlit as st
import os

# Define the SQLite database path using the current directory
#db_file = "Bk_Redbus/bus_data.db" 
db_file = os.path.join(os.getcwd(), 'bus_data.db')  # Adjust the filename as needed

# Connect to SQLite Database
conn = sqlite3.connect(db_file)

# Load the bus data from the SQL table
bus_data = pd.read_sql("SELECT * FROM bus_info", conn)

# Close the database connection
conn.close()

# Title of the app
st.title("Bus Information App")
st.write("Explore available bus routes and details!")

# Get unique routes for dropdown selection
routes = bus_data['Route'].unique()
route_selection = st.selectbox("Select Route:", routes)

# Filter bus data based on selected route
filtered_data = bus_data[bus_data['Route'] == route_selection]

# Shows the number of results 
st.write(f"Showing {len(filtered_data)} results:")

# Sort by option
sort_option = st.selectbox("Sort by:", ["None", "Price", "Rating", "Bus Type"])

# Sorting the filtered data based on user selection
if sort_option == "Price":
    filtered_data = filtered_data.sort_values(by='Price')
elif sort_option == "Rating":
    filtered_data = filtered_data.sort_values(by='Rating', ascending=False)
elif sort_option == "Bus Type":
    filtered_data = filtered_data.sort_values(by='Bus Type')

# Add a serial number starting from 1
filtered_data.reset_index(drop=True, inplace=True)
filtered_data.index += 1  # Start index from 1

# Display the results 
st.dataframe(filtered_data[['Bus Name', 'Start Time', 'End Time', 'Rating', 'Price', 'Bus Type', 'Departure Location', 'Arrival Location', 'Total Duration', 'Seats Available']])





