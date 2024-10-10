# bus_scraper.py

import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Function to scrape bus details
def scrape_bus_data(url):
    driver.get(url)
    time.sleep(3)  # Wait for the page to load

    buses = driver.find_elements(By.CSS_SELECTOR, 'div.result-container')
    bus_data = []

    # Click on "View Buses" button if it exists
    try:
        view_buses_button = driver.find_element(By.XPATH, "//*[@id='result-section']//div[contains(text(), 'View Buses')]")
        view_buses_button.click()
        time.sleep(3)  # Wait for the new content to load
    except Exception as e:
        print("No 'View Buses' button found or error occurred: ", e)

    # Scrape bus details from the current page after clicking "View Buses"
    buses = driver.find_elements(By.CSS_SELECTOR, 'div.result-container')

    for bus in buses:
        try:
            bus_name = bus.find_element(By.CSS_SELECTOR, '.travels.lh-24.f-bold.d-color').text
            start_time = bus.find_element(By.CSS_SELECTOR, '.dp-time.f-19.d-color.f-bold').text
            end_time = bus.find_element(By.CSS_SELECTOR, '.bp-time.f-19.d-color.disp-Inline').text
            rating = bus.find_element(By.XPATH, "//div[@class='rating-sec lh-24']//span").text
            price = bus.find_element(By.CSS_SELECTOR, '.fare.d-block .f-19.f-bold').text
            bus_type = bus.find_element(By.CSS_SELECTOR, '.bus-type').text
            departure_location = bus.find_element(By.XPATH, "//div[@class='dp-loc l-color w-wrap f-12 m-top-42']").text
            arrival_location = bus.find_element(By.XPATH, "//div[@class='bp-loc l-color w-wrap f-12 m-top-8']").text
            total_duration = bus.find_element(By.CSS_SELECTOR, '.dur.l-color.lh-24').text
            seats_available = bus.find_element(By.CSS_SELECTOR, '.seat-left').text

            bus_data.append([bus_name, start_time, end_time, rating, price, bus_type,
                             departure_location, arrival_location, total_duration, seats_available])
        except Exception as e:
            print(f"Error while scraping bus data: {e}")

    return bus_data

# Read completed routes from the text file
with open('completed_routes.txt', 'r') as file:
    urls = [line.strip() for line in file]

# Store the scraped data in a CSV file
with open('bus_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Bus Name", "Start Time", "End Time", "Rating", 
                     "Price", "Bus Type", "Departure Location", "Arrival Location", 
                     "Total Duration", "Seats Available"])

    for url in urls:
        bus_data = scrape_bus_data(url)
        writer.writerows(bus_data)

# Close the driver
driver.quit()
print("Scraping completed and data saved to bus_data.csv.")

