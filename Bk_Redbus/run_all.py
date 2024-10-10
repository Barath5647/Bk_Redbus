import os
import subprocess

# Function to install requirements
def install_requirements():
    print("Installing requirements...")
    subprocess.check_call(["pip", "install", "-r", "requirements.txt"])
    print("Requirements installed.")

# Function to run scripts in sequence
def run_scripts():
    print("Running bus scraper...")
    subprocess.check_call(["python", "bus_scraper.py"])

    print("Running CSV to SQLite...")
    subprocess.check_call(["python", "csv_to_sqlite.py"])

    print("Running Streamlit app...")
    subprocess.Popen(["streamlit", "run", "app.py"])

# Main function
if __name__ == "__main__":
    install_requirements()
    run_scripts()

