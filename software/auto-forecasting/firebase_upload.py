import json
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
import os

def create_json(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f)
    return filepath

# Get environment variables as dictionaries
forecast_key =  json.loads(os.environ['FORECAST_KEY'])

# Create JSON files for the keys
service_account_path = create_json(forecast_key, './serviceAccountKey.json')

# Replace with the URL to your Firebase Realtime Database
database_url = 'https://forecasting-1609-default-rtdb.asia-southeast1.firebasedatabase.app'

# Initialize the Firebase app
try:
  app = firebase_admin.get_app()
except ValueError as e:
  cred = credentials.Certificate(service_account_path)
  app = firebase_admin.initialize_app(cred, {
      'databaseURL': database_url
  })
  
df = pd.read_csv('predictions.csv')

df.to_json('predictions.json', orient='records')

# Replace with the path to your JSON file
json_file_path = 'predictions.json'

# Read the JSON data from the file
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Import the data to your Firebase Realtime Database
root_ref = db.reference('/')
root_ref.set(data)

print('JSON data imported to Firebase successfully.')