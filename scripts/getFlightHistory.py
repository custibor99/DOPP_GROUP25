import pandas as pd
import requests
import urllib.parse
from tqdm import tqdm

# Airlabs
# https://airlabs.co/api/v9/schedules?dep_iata={airport_iata}&api_key={API_KEY}

# FlightAware
# https://www.flightaware.com/live/findflight?origin={dep_iata}&destination={arr_iata}

# Flightradar24
# https://www.flightradar24.com/data/flights/{flight_iata}#{id}


def fetch_airport_schedules(airports):
    API_KEY = input("Enter your API key")
    schedules = []

    for airport_iata in tqdm(airports.index):
        url = f"https://airlabs.co/api/v9/schedules?dep_iata={airport_iata}&api_key={API_KEY}"
        url_parsed = urllib.parse.quote(url, safe="://=?&")
        response = requests.get(url_parsed)

        if response.status_code == 200:
            try:
                schedules.extend(response.json()["response"])
            except Exception as e:
                print(e)

    return pd.DataFrame.from_records(schedules)


# Data doesn't load on initial request from FlightAware. Using Selenium would double the already long load time.
# Web-scraping this way is implausible.
#def fetch_flights_numbers(airport_network):
#    flight_numbers = []
#
#    for route in tqdm(airport_network.edges):
#        origin = airport_network.nodes[route[0]]["iata"]
#        destination = airport_network.nodes[route[1]]["iata"]
#
#        url = f"https://www.flightaware.com/live/findflight?origin={origin}&destination={destination}"
#        url_parsed = urllib.parse.quote(url, safe="://=?&")
#        response = requests.get(url_parsed)
#
#        if response.status_code == 200:
#            try:
#                doc = BeautifulSoup(response.text, 'html.parser')
#                flight_table = doc.find("table", {"id": "Results"})
#                flight_refs = flight_table.find_all("a")
#                flight_numbers.extend([link.get_text() for link in flight_refs])
#                print(flight_numbers)
#
#            except Exception as e:
#                print(e)
#
#    return pd.DataFrame(flight_numbers)


def main():
    airports = pd.read_csv("../data/airport_metadata.csv")
    airports.set_index("IATA airport code", inplace=True)

    schedules = fetch_airport_schedules(airports)
    schedules.to_csv("../data/airport_schedules.csv", index=False)


if __name__ == "__main__":
    main()
