import requests
import networkx as nx 
import pandas as pd 
import numpy as np
import os
from itertools import product
from tqdm import tqdm
import time

SEP = "%7C"
KEY = input("Please enter API key:")

city_data = pd.read_csv("../data/city_coordinates.csv").dropna()
if os.path.isfile("../data/city_car_network.gml"):
    G = nx.read_gml("../data/city_car_network.gml")
else:
    G = nx.Graph()

all_cities = city_data["city"].unique()
all_ids = city_data["place_id"].unique()

map = { key:val for key, val in  zip(all_ids, all_cities)}
for source in tqdm(all_ids):
    destination = [ f"place_id:{place}" for place in all_ids if not G.has_edge(map[source], map[place])]
    n_iters = int(np.ceil(len(destination) / 25))
    for i in range(0, n_iters):
        destination_subset = destination[i*25:(i+1)*25]
        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?destinations={SEP.join(destination_subset)}&origins=place_id:{source}&key={KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            for i, place in enumerate(destination_subset):
                if response.json()["rows"][0]["elements"][i]["status"] == "OK":
                    distance = response.json()["rows"][0]["elements"][i]["distance"]["value"] 
                    duration = response.json()["rows"][0]["elements"][i]["duration"]["value"]
                    G.add_edge(map[source], map[place.replace("place_id:","")], distance=distance, duration=duration)
    nx.write_gml(G, "../data/city_car_network.gml")
    time.sleep(0.5)
