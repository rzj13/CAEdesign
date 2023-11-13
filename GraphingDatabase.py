import requests
import json
import time
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

# Initialize Firebase
cred_object = firebase_admin.credentials.Certificate('C:\\Users\\ryanz\Desktop\\SD Proj\\AccountKey.json')
default_app = firebase_admin.initialize_app(cred_object, {
'databaseURL': 'https://senior-design-test-78c5a-default-rtdb.firebaseio.com/'
})

# Function to fetch and parse the JSON response from the local API
def get_temperature():
    try:
        url = "http://10.0.0.183/api/values"  # Replace with your actual local API URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the JSON response
        data = json.loads(response.text)
        temperature = data['modules'][0]['Celsius']

        return temperature
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to write temperature data to the Firebase Realtime Database
def write_temperature_to_database(temperature):
    try:
        table = "temperature_data"  # Replace with the desired Firebase database table
        timestamp = int(time.time())  # Get the current UNIX timestamp
        ref = db.reference(table)

        # Create a JSON object to write to the database
        data = {
            'temperature': temperature,
            'time': timestamp
        }

        ref.push(data)  # Push the data to the database

        print(f"Temperature {temperature} °C written to the database at timestamp {timestamp}")
    except Exception as e:
        print(f"Error: {e}")

# Main loop to continuously fetch temperature and write it to the database
while True:
    temperature = get_temperature()
    if temperature is not None:
        write_temperature_to_database(temperature)

    # Wait for a few seconds before fetching the next temperature
    time.sleep(5)  # Adjust the delay time (in seconds) as needed
