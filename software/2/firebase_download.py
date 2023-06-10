import requests
import json
import csv
import time

forecast_url = "https://forecasting-1609-default-rtdb.asia-southeast1.firebasedatabase.app/.json"

# Set the number of retries and delay between retries
max_retries = 5
retry_delay = 1

# Function to download data from Firebase
def download_data(url):
    for retry_count in range(max_retries):
        try:
            response = requests.get(url, timeout=20)
            break
        except requests.exceptions.RequestException:
            print(f"Connection failed, retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
    else:
        print("Failed to establish a connection to the Firebase Realtime Database.")
        exit()

    return json.loads(response.content)

# Download generation and weather data from Firebase
consumption_data = download_data(forecast_url)

# Save generation data to CSV
with open("household_power_consumption.csv", "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["Global_active_power", "Global_reactive_power", "Voltage", "Global_intensity", "Sub_metering_1", "Sub_metering_2", "Sub_metering_3"])
    for value in consumption_data:
        writer.writerow([value["Global_active_power"], value["Global_reactive_power"], value["Voltage"], value["Global_intensity"], value["Sub_metering_1"], value["Sub_metering_2"], value["Sub_metering_3"]])
