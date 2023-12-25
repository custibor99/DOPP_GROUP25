import requests
import networkx as nx 
import pandas as pd 
import numpy as np
from itertools import product
from tqdm import tqdm


KEY = input("Please enter api key:")

airport_data = pd.read_csv("../data/airport_metadata.csv")
res = {
    "iata_code": [],
    "lat": [],
    "lng": []
}
all_codes = list(airport_data["IATA airport code"].unique())
for iata_code in tqdm(all_codes):
    url = f"https://airlabs.co/api/v9/airports?iata_code={iata_code}&api_key={KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            geo = response.json()["response"]
            res["lat"].append(geo[0]["lat"])
            res["lng"].append(geo[0]["lng"])
            res["iata_code"].append(iata_code)
        except:
            pass

pd.DataFrame(res).to_csv("../data/airportCoordinates.csv", index=False)