import pandas as pd
import networkx as nx
import numpy as np
import time 
from tqdm import tqdm
from itertools import product
import requests
import urllib.parse
import json
import requests


def get_weight(id1: int, id2: int) -> int:
    res = 9999999
    url = f"https://www.chronotrains.com/api/trip/{id1}/{id2}"
    url_parsed = urllib.parse.quote(url, safe="://")
    response = requests.get(url_parsed)
    if response.status_code == 200:
        try:
            json_response = response.json()
            with open(f'data/json_data/{id1}_to_{id2}.json', 'w') as f:
                json.dump(json_response, f)
        except:
            pass
        try:
            res = json_response["suggestion"]["duration"]
        except:
            pass
    return res

def main():
    try:
        G = nx.read_gml("../data/city_train_network_duration.gml")
    except:
        G = nx.read_gml("../data/city_train_network.gml")
        
    edges = list(G.edges)
    city_id_map = nx.get_node_attributes(G, "chronotrain_id")
    i = 0
    for node1, node2 in tqdm(edges):
        #Get chronotrain ids
        id1 = int(city_id_map[node1])
        id2 = int(city_id_map[node2])
        
        #check if weight exist
        try:
            weight = G[node1][node2]["weight"]
        except:
            weight = get_weight(id1, id2)
            G[node1][node2]["weight"] = weight    
            i += 1
            time.sleep(0.5)
        
        #save to file every 15 iterations
        if i % 15 == 0:
            nx.write_gml(G, "../data/city_train_network_duration.gml")
        
    
    #Save to file in the end
    nx.write_gml(G, "../data/city_train_network_duration.gml")

if __name__ == "__main__":
    main()
