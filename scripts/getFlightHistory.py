import networkx as nx
import pandas as pd
import requests
import urllib.parse
import os
from tqdm import tqdm

# Airlabs
# https://airlabs.co/api/v9/schedules?dep_iata={airport_iata}&api_key={API_KEY}

# FlightAware
# https://www.flightaware.com/live/findflight?origin={dep_iata}&destination={arr_iata}

# Flightradar24
# https://www.flightradar24.com/data/flights/{flight_iata}#{id}


# Free plan only gives max 50 routes per airport. Full route map cannot be constructed this way due to missing routes.
def fetch_routes(airports, api_key):
    routes = []

    for airport_iata in tqdm(airports.index):
        url = f"https://airlabs.co/api/v9/routes?dep_iata={airport_iata}&api_key={api_key}"
        url_parsed = urllib.parse.quote(url, safe="://=?&")
        response = requests.get(url_parsed)

        if response.status_code == 200:
            try:
                routes.extend(response.json()["response"])
            except Exception as e:
                print(e)

    return pd.DataFrame.from_records(routes)


def fetch_schedules(airports, api_key):
    schedules = []

    for airport_iata in tqdm(airports.index):
        url = f"https://airlabs.co/api/v9/schedules?dep_iata={airport_iata}&api_key={api_key}"
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

    airport = nx.read_gml("../data/airport_network.gml")
    city = nx.read_gml("../data/city_train_network_duration.gml")

    api_key = input("Enter your API key")

#    if not os.path.isfile("..data/airport_routes.csv"):
#        routes = fetch_routes(airports, api_key)

    schedules = fetch_schedules(airports, api_key)

    if os.path.isfile("../data/airport_schedules.csv"):
        schedules_cached = pd.read_csv("../data/airport_schedules.csv")
        schedules = pd.concat([schedules_cached, schedules])

    schedules.to_csv("../data/airport_schedules.csv", index=False)


if __name__ == "__main__":
    main()
