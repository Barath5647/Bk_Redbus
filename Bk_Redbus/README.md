# Bk_Redbus Project

This project scrapes bus data from RedBus, stores it in an SQLite database, and displays the data in a Streamlit web application. The project is built using Python, Selenium, Pandas, SQLite, and 
Streamlit.

## Project Structure

- **bus_scraper.py**: Scrapes bus data from RedBus based on the URLs in `completed_routes.txt`.
- **csv_to_sqlite.py**: Converts the scraped CSV data into an SQLite database.
- **app.py**: Streamlit application to display the bus data in a web interface.
- **bus_data.csv**: The CSV file where the scraped bus data is stored.
- **bus_data.db**: SQLite database created from the CSV file.
- **completed_routes.txt**: Contains the list of RedBus URLs for scraping.
- **requirements.txt**: Contains the required libraries for the project.
- **run_all.py**: Script to install dependencies and run the project step by step.

## Setup Instructions

1. **Clone the Repository**:  
   Download the project files to your local machine.

2. **Install Requirements**:
   Open a terminal, navigate to the project folder, and run the following command:
   ```bash
   python run_all.py


