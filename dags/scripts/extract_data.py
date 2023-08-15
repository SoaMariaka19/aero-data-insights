import requests
import json
from datetime import datetime
import os

def load_api_key():
    script_folder = os.path.dirname(os.path.abspath(__file__))
    config_folder = os.path.join(script_folder, 'config')
    api_config_path = os.path.join(config_folder, 'api_config.json')

    with open(api_config_path, 'r') as config_file:
        config_data = json.load(config_file)
        return config_data.get('API_KEY')

def extract_flight_data(api_key):
    url = "https://test.api.amadeus.com/v2/f/shopping/flight-offers"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch flight data")

if __name__ == "__main__":
    api_key = load_api_key()
    flight_data = extract_flight_data(api_key)
    filename = f"flight_data_{datetime.now().strftime('%Y_%m_%d')}.json"
    with open(filename, "w") as f:
        json.dump(flight_data, f)
