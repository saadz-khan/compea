import requests
import json
import csv
import time

generation_url = "https://esp-firebase-demo-103cc-default-rtdb.asia-southeast1.firebasedatabase.app/.json"
weather_url = "https://weather-1609-default-rtdb.asia-southeast1.firebasedatabase.app/.json"

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
generation_data = download_data(generation_url)
weather_data = download_data(weather_url)

# Save generation data to CSV
with open("generation_data.csv", "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["DATE_TIME", "PLANT_ID", "SOURCE_KEY", "DC_POWER", "AC_POWER", "DAILY_YIELD", "TOTAL_YIELD"])
    for value in generation_data:
        writer.writerow([value["DATE_TIME"], value["PLANT_ID"], value["SOURCE_KEY"], value["DC_POWER"], value["AC_POWER"], value["DAILY_YIELD"], value["TOTAL_YIELD"]])

# Save weather data to CSV
with open("weather_data.csv", "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["DATE_TIME", "PLANT_ID", "SOURCE_KEY", "AMBIENT_TEMPERATURE", "MODULE_TEMPERATURE", "IRRADIATION"])
    for value in weather_data:
        writer.writerow([value["DATE_TIME"], value["PLANT_ID"], value["SOURCE_KEY"], value["AMBIENT_TEMPERATURE"], value["MODULE_TEMPERATURE"], value["IRRADIATION"]])