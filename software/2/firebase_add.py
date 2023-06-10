import json
import os
import firebase_admin
from firebase_admin import credentials, db

def create_json(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f)
    return filepath

# Get environment variables as dictionaries
weather_key =  json.loads(os.environ['WEATHER_KEY'])
generation_key =  json.loads(os.environ['GENERATION_KEY'])

# Create JSON files for the keys
weather_key_path = create_json(weather_key, './weather_key.json')
generation_key_path = create_json(generation_key, './generation_key.json')

weather_data_filepath = './data/4w_weather.json'
generation_data_filepath = './data/4w_generation.json'

weather_url = "https://weather-1609-default-rtdb.asia-southeast1.firebasedatabase.app"
generation_url = 'https://esp-firebase-demo-103cc-default-rtdb.asia-southeast1.firebasedatabase.app'

# Initialize the Weather Firebase app
weather_cred = credentials.Certificate(weather_key_path)
weather_app = firebase_admin.initialize_app(weather_cred, {
    'databaseURL': weather_url
}, name='weather_app')

# Read the JSON data from the weather file
with open(weather_data_filepath, 'r') as file:
    data = json.load(file)

# Import the data to your Weather Firebase Realtime Database
root_ref = db.reference('/', app=weather_app)
root_ref.set(data)

# Initialize the Generation Firebase app
generation_cred = credentials.Certificate(generation_key_path)
generation_app = firebase_admin.initialize_app(generation_cred, {
    'databaseURL': generation_url
}, name='generation_app')

# Read the JSON data from the generation file
with open(generation_data_filepath, 'r') as file:
    data = json.load(file)

# Import the data to your Generation Firebase Realtime Database
root_ref = db.reference('/', app=generation_app)
root_ref.set(data)

print('JSON data imported to Firebase successfully.')
