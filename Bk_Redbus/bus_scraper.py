import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

# Initialize the Chrome driver
driver = webdriver.Chrome()


# Set up the current working directory
output_directory = os.getcwd()
completed_routes_file = os.path.join(output_directory, "completed_routes.txt")
csv_file = os.path.join(output_directory, "bus_data.csv")

# Function to scroll down the page until the end 
def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
        time.sleep(2) 
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:  
            break
        last_height = new_height

# Function to gather route links from each state (for completed_routes.txt)
def gather_route_links():
    driver.get("https://www.redbus.in/online-booking/rtc-directory")
    
    #scroll_to_bottom()
    state_links = driver.find_elements(By.CSS_SELECTOR, "a.D113_link")  
    
    routes = []
    
    for state_link in state_links:
        try:
            state_name = state_link.text
            print(f"Gathering routes for {state_name}...")
            
            
            state_link.click()
            time.sleep(5)  
            scroll_to_bottom()
            
            # Find route links
            route_links = driver.find_elements(By.CSS_SELECTOR, "a.route")
            for route_link in route_links:
                route_name = route_link.text
                route_url = route_link.get_attribute('href')
                routes.append(route_url)
            
            # Go back to RTC directory
            driver.back()
            time.sleep(5)
        except Exception as e:
            print(f"Error gathering routes for {state_name}: {e}")
    
    return routes

# Function to save route links to completed_routes.txt
def save_routes_to_file():
    routes = gather_route_links()
    
    
    with open(completed_routes_file, mode="w", encoding="utf-8") as file:
        for route in routes:
            file.write(route + "\n")
    
    print(f"Saved {len(routes)} routes to {completed_routes_file}")

# Function to scrape bus details for each route
def scrape_bus_data(url):
    driver.get(url)
    time.sleep(3)  
    
    bus_data = []

    # Click on "View Buses" button if it exists
    try:
        view_buses_button = driver.find_element(By.XPATH, "//*[@id='result-section']//div[contains(text(), 'View Buses')]")
        view_buses_button.click()
        time.sleep(3)  
    except Exception as e:
        print("No 'View Buses' button found or error occurred: ", e)

    scroll_to_bottom()   # Scroll till the end of the page to load all buses
    
    
    buses = driver.find_elements(By.CSS_SELECTOR, '.result-sec')

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

# Step 1: Gather routes and save to completed_routes.txt
save_routes_to_file()

# Step 2: Read the completed routes from the text file
with open('completed_routes.txt', 'r') as file:
    urls = [line.strip() for line in file]

# Step 3: Store the scraped data in a CSV file
with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
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

