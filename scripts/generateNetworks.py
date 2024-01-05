import pandas as pd
import networkx as nx
import numpy as np
import time 
from itertools import product
import FlightEstimator

def get_neighbors_by_country_code(country_metadata:pd.DataFrame, iso_code: str) -> list:
    n = country_metadata.query(f"iso_country_code == '{iso_code}'")["neighbors"].values[0]
    res = []
    try:
        res = n.split(",")
    except:
        pass
    return res

def generate_country_network(country_metadata: pd.DataFrame) -> nx.Graph:
    G = nx.Graph()
    for code in country_metadata["iso_country_code"].unique():
        neighbor_codes = get_neighbors_by_country_code(country_metadata, code)
        for n in neighbor_codes:
            G.add_edge(code, n)
    return G

def generate_city_network(country_network, country_metadata, chronotrain_data)-> nx.Graph:
    merged = chronotrain_data.merge(country_metadata, on="Country").dropna()
    city_network = nx.Graph()
    for id, city in merged[["chronotrain_id", "city"]].values:
        city_network.add_nodes_from([(city, {"chronotrain_id":id})])
    
    countries = list(country_network.nodes) 
    merged = merged.dropna()
    for country in countries:
        #Build internal network of country
        cities_in_country = list(merged.query(f"iso_country_code == '{country}'")["city"].values)
        prod = product(cities_in_country, cities_in_country)
        edges = [(c1, c2) for c1, c2 in prod if c1 != c2]
        for c1, c2 in edges:
            city_network.add_edge(c1,c2)
    
        #Build connections to neighbors
        neighbors = set(country_network[country])
        neighbor_cities = list(merged["city"].loc[merged["iso_country_code"].isin(neighbors)].values)
        prod = product(cities_in_country, neighbor_cities)
        edges = [(c1, c2) for c1, c2 in prod if c1 != c2]
        for c1, c2 in edges:
            city_network.add_edge(c1,c2)
            
    return city_network

def generate_airport_network(airport_data):
    airport_network = nx.Graph()

    airport_network.add_nodes_from(
        [(iata, {"city": city}) for (iata, city) in list(zip(airport_data['iata_code'], airport_data['city']))])
    skipped = 0
    for idx_place, place in airport_data.iterrows():
        for idx_dest, dest in airport_data.iterrows():

            # Graph is undirected with no self loops.
            if airport_network.has_edge(place["iata_code"], dest["iata_code"]) or place["iata_code"] == dest["iata_code"]:
                continue

            distance = FlightEstimator.calculate_distance(place["lat"], place["lng"], dest["lat"], dest["lng"])
            if distance < FlightEstimator.distance_threshhold:
                airport_network.add_edge(place["iata_code"], dest["iata_code"], distance=distance)
            else:
                skipped += 1

    print(f"Airport Network: Skipped {skipped} edges that where outside of the distance threshhold. "
          f"Graph has {airport_network.number_of_nodes()} nodes (airports) and {airport_network.number_of_edges()} edges (routes)")
    return airport_network

def main():
    country_metadata = pd.read_csv("../data/country_metadata.csv")
    chronotrain_data = pd.read_csv("../data/chronotrains.csv")

    airport_metadata = pd.read_csv("../data/airport_metadata.csv")
    airport_coordinates = pd.read_csv("../data/airport_coordinates.csv")
    airport_data = airport_metadata.merge(airport_coordinates, left_on="IATA airport code", right_on="iata_code")
    
    start = time.time()
    G = generate_country_network(country_metadata)
    nx.write_gml(G, "../data/country_network.gml")
    end = time.time()
    print(f"Generated file data/country_network.txt in {end-start} seconds") 

    start = time.time()
    city_network = generate_city_network(G, country_metadata, chronotrain_data)
    nx.write_gml(city_network, "../data/city_train_network.gml")
    end = time.time()
    print(f"Generated file data/country_network.txt in {end-start} seconds")

    start = time.time()
    airport_network = generate_airport_network(airport_data)
    nx.write_gml(airport_network, "../data/airport_network.gml")
    end = time.time()
    print(f"Generated file data/airport_network.gml in {round(end - start, 2)} seconds")


if __name__ == "__main__":
    main()
    
    
