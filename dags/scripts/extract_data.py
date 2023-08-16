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
    params= {
        'originLocationCode': 'MD',
        'destinationLocationCode': 'AF',
        'departureDate': '2023-05-02',
        'returnDate': '2023-07-28',
        'adults': 12,
        'children': 10,
        'infants': 2,
        'travelClass': 'ECONOMY',
        'includedAirlineCode': 'MD',
        'excludedAirlineCodes': 'AF',
        'nonStop': 'false',
        'currencyCode': 'EUR',
        'maxPrice': 10,
        'max': 250
    }
    response = requests.get(url,params=params, headers=headers)

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


def extract_airport_city_search(api_key):
    url = "https://test.api.amadeus.com/v1/f/reference-data/locations"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {
        'subType': 'AIRPORT',
        'keyword': 'MAD',
        'countryCode': 'MG',
        'page[limit]': 4,
        'page[offset]': 2,
        'sort': 'analytics.travelers.score',
        'view': 'LIGHT'
    }
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch airport or city data")

if __name__ == "__main__":
    api_key = load_api_key()
    
    airport_city_search = extract_airport_city_search(api_key)

    airport_city_filename = f"airport_city_data_{datetime.now().strftime('%Y_%m_%d')}.json"
    with open(airport_city_filename, "w") as f:
        json.dump(airport_city_search, f, indent=4)  

def extract_spec_airport_city_search(api_key):
    url = "https://test.api.amadeus.com/v1/f/reference-data/locations/{locationId}"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {
        'locationId': 'MG'
    }
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch specific airport or city data")

if __name__ == "__main__":
    api_key = load_api_key()
    
    spec_airport_city_search = extract_spec_airport_city_search(api_key)

    spec_airport_city_filename = f"spec_airport_city_data_{datetime.now().strftime('%Y_%m_%d')}.json"
    with open(spec_airport_city_filename, "w") as f:
        json.dump(spec_airport_city_search, f, indent=4)  

def extract_flight_dates(api_key):
    url = "https://test.api.amadeus.com/v1/f/shopping/flight-dates"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {
    'origin': 'MD',  
    'destination': 'AF',
    'departureDate': '2023-08-16',  
    'oneWay': 'true',
    'duration': 2.8, 
    'nonStop': 'false',
    'maxPrice': 10,
    'viewBy': 'DATE'
    }
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch flight dates data")

if __name__ == "__main__":
    api_key = load_api_key()
    
    flight_cheapest_date_search = extract_flight_dates(api_key)
    flight_date_filename = f"flight_date_data_{datetime.now().strftime('%Y_%m_%d')}.json"
    with open(flight_date_filename, "w") as f:
        json.dump(flight_cheapest_date_search, f, indent=4)  

def extract_flight_price_analysis_data(api_key):
    url = "https://test.api.amadeus.com/v1/f//analytics/itinerary-price-metrics"
    headers = {"Authorization": f"Bearer {api_key}"}
    params= {
        'originIataCode': 'MD',
        'destinationIataCode': 'AF',
        'departureDate': '2021-03-21',
        'currencyCode': 'AF',
        'oneWay': 'true'
    }
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch flight prices data")

if __name__ == "__main__":
    api_key = load_api_key()
    
    flight_price_analysis = extract_flight_price_analysis_data(api_key)
    flight_price_filename = f"flight_price_data_{datetime.now().strftime('%Y_%m_%d')}.json"
    with open(flight_price_filename, "w") as f:
        json.dump(flight_price_analysis, f, indent=4)  