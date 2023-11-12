import requests
import json
import time

# URL of the API endpoint
url = "http://10.0.0.183/api/values/128"  # Replace with your actual local API URL

# Function to fetch and parse the JSON response
def get_temperature():
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for any HTTP errors
        
        # Parse the JSON response
        data = json.loads(response.text)
        
        # Extract the temperature value from the JSON
        temperature = data['modules'][0]['Celsius']  # Assuming the temperature is under 'Celsius' key
        
        return temperature
    except Exception as e:
        print(f"Error: {e}")
        return None

# Main loop to continuously fetch and print temperature data
while True:
    temperature = get_temperature()
    if temperature is not None:
        print(f"Current Temperature: {temperature} °C")
    
    # Wait for a few seconds before refreshing the data
    time.sleep(5)  # Adjust the delay time (in seconds) as needed
