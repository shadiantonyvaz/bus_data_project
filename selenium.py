import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# List of RedBus URLs
urls = [
    'https://www.redbus.in/bus-tickets/pune-to-goa?fromCityId=130&toCityId=210&fromCityName=Pune&toCityName=Goa&busType=Any&opId=7115&onward=05-Sep-2024',
    'https://www.redbus.in/bus-tickets/tirupathi-to-bangalore?fromCityId=71756&toCityId=122&fromCityName=Tirupati&toCityName=Bangalore&busType=Any&opId=10283&onward=05-Sep-2024',
    'https://www.redbus.in/bus-tickets/delhi-to-shimla?fromCityId=733&toCityId=1285&fromCityName=Delhi&toCityName=Shimla&busType=Any&opId=16227&onward=05-Sep-2024',
    'https://www.redbus.in/bus-tickets/visakhapatnam-to-vijayawada?fromCityId=248&toCityId=134&fromCityName=Visakhapatnam&toCityName=Vijayawada&busType=Any&opId=10283&onward=05-Sep-2024',
    'https://www.redbus.in/bus-tickets/tirupathi-to-chennai?fromCityId=71756&toCityId=123&fromCityName=Tirupati&toCityName=Chennai&busType=Any&opId=10283&onward=05-Sep-2024',
    'https://www.redbus.in/bus-tickets/khammam-to-hyderabad?fromCityId=401&toCityId=124&fromCityName=Khammam&toCityName=Hyderabad&busType=Any&opId=18491&onward=05-Sep-2024',
    'https://www.redbus.in/bus-tickets/bangalore-to-chennai?fromCityId=122&toCityId=123&fromCityName=Bangalore&toCityName=Chennai&busType=Any&srcCountry=IND&destCountry=IND&onward=05-Sep-2024',
    'https://www.redbus.in/bus-tickets/kodad-to-hyderabad?fromCityId=91366&toCityId=124&fromCityName=Kodad&toCityName=Hyderabad&busType=Any&opId=18491&onward=05-Sep-2024',
    'https://www.redbus.in/bus-tickets/salem-to-chennai?fromCityId=602&toCityId=123&fromCityName=Salem&toCityName=Chennai&busType=Any&onward=05-Sep-2024',
    'https://www.redbus.in/bus-tickets/tiruchirapalli-to-chennai?fromCityId=71929&toCityId=123&fromCityName=Tiruchirapalli&toCityName=Chennai&busType=Any&onward=05-Sep-2024',
    'https://www.redbus.in/bus-tickets/vijayawada-to-hyderabad?fromCityId=134&toCityId=124&fromCityName=Vijayawada&toCityName=Hyderabad&busType=Any&opId=10283&onward=05-Sep-2024'
]

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

# Lists to hold all data
bus_routes = []
bus_names = []
bus_types = []
prices = []
departing_times = []
durations = []
arriving_times = []
ratings = []
seats_available = []
route_links = []

for url in urls:
    driver.get(url)
    time.sleep(5)  # Adjust wait time as necessary

    # Wait until the bus route name element is present
    wait = WebDriverWait(driver, 20)
    bus_route_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='h2-tag-seo']")))
    bus_route = bus_route_element.text.strip()

    # Scroll to the bottom of the page to load all elements
    body = driver.find_element(By.CSS_SELECTOR, "body")
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        body.send_keys(Keys.END)
        time.sleep(2)  # Adjust wait time as necessary
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Wait until the bus elements are present
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".travels.lh-24.f-bold.d-color")))

    # Get all bus details
    bus_names_elements = driver.find_elements(By.CSS_SELECTOR, ".travels.lh-24.f-bold.d-color")
    bus_types_elements = driver.find_elements(By.CSS_SELECTOR, ".bus-type.f-12.m-top-16.l-color")
    prices_elements = driver.find_elements(By.CSS_SELECTOR, ".fare.d-block")
    departing_times_elements = driver.find_elements(By.CSS_SELECTOR, ".dp-time.f-19.d-color.f-bold")
    durations_elements = driver.find_elements(By.CSS_SELECTOR, ".dur.l-color.lh-24")
    arriving_times_elements = driver.find_elements(By.CSS_SELECTOR, ".bp-time.f-19.d-color.disp-Inline")
    ratings_elements = driver.find_elements(By.CSS_SELECTOR, '.rating-sec.lh-24 span')
    seats_available_elements = driver.find_elements(By.CSS_SELECTOR, ".column-eight.w-15.fl .seat-left.m-top-30")

    # Extract data
    for bus_name, bus_type, price, departing_time, duration, arriving_time, rating, seats in zip(
            bus_names_elements, bus_types_elements, prices_elements, departing_times_elements,
            durations_elements, arriving_times_elements, ratings_elements, seats_available_elements):
        bus_routes.append(bus_route)
        bus_names.append(bus_name.text.strip())
        if bus_type:
            bus_types.append(bus_type.text.strip())
        else:
            bus_types.append('Unknown')  # Handle missing bus type
        prices.append(price.text.strip())
        departing_times.append(departing_time.text.strip())
        durations.append(duration.text.strip())
        arriving_times.append(arriving_time.text.strip())
        ratings.append(rating.text.strip())

        # Extract seats availability, handling missing data
        if seats.text:
            seats_available.append(seats.text.strip().split()[0])
        else:
            seats_available.append('Unknown')

        route_links.append(url)

# Close the WebDriver
driver.quit()

# Create a DataFrame
df = pd.DataFrame({
    'Bus Route': bus_routes,
    'Bus Name': bus_names,
    'Bus Type': bus_types,
    'Price': prices,
    'Departing Time': departing_times,
    'Duration': durations,
    'Arriving Time': arriving_times,
    'Rating': ratings,
    'Seats Available': seats_available,
    'Route Link': route_links
})

# Save DataFrame to CSV
df.to_csv('/Users/shadivaz/Desktop/all_combined_bus_data.csv', index=False)

# Display the DataFrame
print(df.head())
