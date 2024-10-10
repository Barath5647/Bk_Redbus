import pandas as pd
import sqlite3
import os

# Define the correct path for the CSV file (use relative path)
csv_file = os.path.join(os.getcwd(), 'bus_data.csv')  # Ensure this file exists
db_file = os.path.join(os.getcwd(), 'bus_data.db')  # SQLite database path

# Step 1: Load CSV Data
bus_data = pd.read_csv(csv_file)

# Step 2: Connect to SQLite Database (will create if not exists)
conn = sqlite3.connect(db_file)

# Step 3: Convert DataFrame to SQL table
bus_data.to_sql("bus_info", conn, if_exists="replace", index=False)

# Close the database connection
conn.close()

print("CSV data has been successfully converted and stored in SQLite database.")

