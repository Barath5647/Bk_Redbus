import pandas as pd
import sqlite3
import streamlit as st
import os

# Define the SQLite database path using the current directory
db_file = "Bk_Redbus/bus_data.db" #db_file = os.path.join(os.getcwd(), 'bus_data.db')  # Adjust the filename as needed

# Connect to SQLite Database
conn = sqlite3.connect(db_file)

# Load the bus data from the SQL table
bus_data = pd.read_sql("SELECT * FROM bus_info", conn)

# Close the database connection
conn.close()

# Title of the app
st.title("Bus Information App")
st.write("Explore available bus routes and details!")

# --- New Filter Options ---

# 1. Route filter
routes = bus_data['Route'].unique()
route_selection = st.selectbox("Select Route:", ["All"] + list(routes))

# 2. Price filter (using a slider to select price range)
min_price, max_price = st.slider("Select Price Range:", 0, int(bus_data['Price'].max()), (0, int(bus_data['Price'].max())))

# 3. Rating filter (using a slider for star ratings)
min_rating = st.slider("Select Minimum Rating:", 0.0, 5.0, 0.0, 0.1)

# 4. Bus Type filter (select multiple bus types)
bus_types = bus_data['Bus Type'].unique()
bus_type_selection = st.multiselect("Select Bus Type(s):", bus_types)

# --- Building Dynamic SQL Query ---

# Initialize query with base query
query = "SELECT * FROM bus_info WHERE 1=1"

# Apply Route filter
if route_selection != "All":
    query += f" AND Route = '{route_selection}'"

# Apply Price filter
query += f" AND Price >= {min_price} AND Price <= {max_price}"

# Apply Rating filter
query += f" AND Rating >= {min_rating}"

# Apply Bus Type filter (if multiple bus types are selected)
if bus_type_selection:
    bus_types_str = ",".join([f"'{bt}'" for bt in bus_type_selection])
    query += f" AND BusType IN ({bus_types_str})"

# Execute the dynamic query
conn = sqlite3.connect(db_file)
filtered_data = pd.read_sql(query, conn)
conn.close()

# --- Display Filtered Results ---
st.write(f"Showing {len(filtered_data)} results:")

# Add a serial number starting from 1
filtered_data.reset_index(drop=True, inplace=True)
filtered_data.index += 1  # Start index from 1

# Display the filtered results
st.dataframe(filtered_data[['Bus Name', 'Start Time', 'End Time', 'Rating', 'Price', 'Bus Type', 'Departure Location', 'Arrival Location', 'Total Duration', 'Seats Available']])




























# # Get unique routes for dropdown selection
# routes = bus_data['Route'].unique()
# route_selection = st.selectbox("Select Route:", routes)

# # Filter bus data based on selected route
# filtered_data = bus_data[bus_data['Route'] == route_selection]

# # Shows the number of results 
# st.write(f"Showing {len(filtered_data)} results:")

# # Sort by option
# sort_option = st.selectbox("Sort by:", ["None", "Price", "Rating", "Bus Type"])

# # Sorting the filtered data based on user selection
# if sort_option == "Price":
#     filtered_data = filtered_data.sort_values(by='Price')
# elif sort_option == "Rating":
#     filtered_data = filtered_data.sort_values(by='Rating', ascending=False)
# elif sort_option == "Bus Type":
#     filtered_data = filtered_data.sort_values(by='Bus Type')

# # Add a serial number starting from 1
# filtered_data.reset_index(drop=True, inplace=True)
# filtered_data.index += 1  # Start index from 1

# # Display the results 
# st.dataframe(filtered_data[['Bus Name', 'Start Time', 'End Time', 'Rating', 'Price', 'Bus Type', 'Departure Location', 'Arrival Location', 'Total Duration', 'Seats Available']])





