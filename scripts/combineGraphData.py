import pandas as pd
import networkx as nx

def add_airports_to_graph(G: nx.Graph, airport_data:pd.DataFrame) -> nx.Graph:
    for row in airport_data.iterrows():
        G.add_node(row[1]["iata_code"], 
                   type="Airport",
                   name=row[1]["Airport"],
                   pos=(row[1]["airport_lat"], row[1]["airport_lng"]),
                   icao=row[1]["icao_code"],
                   iata=row[1]["iata_code"])
    return G

def add_cities_to_graph(G: nx.Graph, city_data: pd.DataFrame) -> nx.Graph:
    for row in city_data.iterrows():
        val  = row[1]
        G.add_node(val["city"],type="City", name=val["city"], pos=(val["city_lat"], val["city_lng"]))
    return G

def add_stations_to_graph(G: nx.Graph, station_data: pd.DataFrame) -> nx.Graph:
    for row in station_data.iterrows():
        val = row[1]
        G.add_node(val["city"]+" Station", city = val["city"], type="Station", id = int(val["chronotrain_id"]), pos=(val["train_station_lat"], val["train_station_lng"]))
    return G

def add_train_durations(G: nx.Graph, train_graph: nx.Graph) -> nx.Graph:
    for source, dest in train_graph.edges:
        duration = train_graph[source][dest]["weight"]
        source = source + " Station"
        dest = dest + " Station"
        if G.has_node(source) and G.has_node(dest):
            try:
                if G.nodes[source]["type"] == "Station" and G.nodes[dest]["type"] == "Station":
                    G.add_edge(source, dest, duration=duration, type="train")
            except:
                pass
    return G

def add_car_durations(G: nx.Graph, car_graph: nx.Graph): 
    for source, dest in car_graph.edges:
        duration = round(car_graph[source][dest]["duration"] / 60)
        distance = round(car_graph[source][dest]["distance"] / 1000)
        if G.has_node(source) and G.has_node(dest) and duration != 0:
            G.add_edge(source, dest, duration=duration, distance=distance, type="car")
    return G

def add_plane_durations(G: nx.Graph, plane_network: nx.Graph) -> nx.Graph:
    for source, dest in plane_network.edges:
        duration = round(plane_network[source][dest]["duration"])
        distance = round(plane_network[source][dest]["distance"] / 1000)
        if G.has_node(source) and G.has_node(dest) and duration != 0:
            G.add_edge(source, dest, duration=duration, distance=distance, type="plane")
    return G

def add_city_to_location_durations(G: nx.Graph, all_data: pd.DataFrame) -> nx.Graph:
    for row in all_data.iterrows():
        val = row[1]
        iata_code = val["iata_code"]
        city = val["city"]
        station = city + " Station"
        G.add_edge(city, station, duration=val["station_duration"], type="car")
        G.add_edge(city, iata_code, duration=val["airport_duration"], type="car")
    return G
    
def main():
    df = pd.read_csv("../data/clean/all_data.csv")
    mask = df["station_duration"] <= 250
    df = df.loc[mask]
    df.to_csv("../data/clean/all_data.csv")
    airport_data = df[["Airport", "iata_code", "icao_code", "airport_lat", "airport_lng"]].drop_duplicates()
    city_data = df[["city", "city_lat", "city_lng"]].drop_duplicates()
    station_data = df[["city", "chronotrain_id", "train_station_lat", "train_station_lng"]].drop_duplicates()
    
    train_graph = nx.read_gml("../data/city_train_network_duration.gml")
    car_graph = nx.read_gml("../data/city_car_network.gml")
    plane_network = nx.read_gml("../data/airport_network.gml")
    
    G = nx.Graph()
    G = add_airports_to_graph(G, airport_data)
    G = add_cities_to_graph(G, city_data)
    G = add_stations_to_graph(G, station_data)
    G = add_train_durations(G, train_graph)
    G = add_car_durations(G, car_graph)
    G = add_plane_durations(G, plane_network)
    G = add_city_to_location_durations(G, df)
    G.remove_node("Lyon-St")
    G.remove_node("Athens")
    G.remove_node("Podgorica")
    G.remove_node("Skopje")
    G.remove_node("Belgrade")
    G.remove_node("Ankara")
    G.remove_node("Istanbul")
    G.remove_node("Izmir")
    G.remove_node("Thessaloniki")
    nx.write_gml(G, "../data/clean/all_routes.gml")

if __name__ == "__main__":
    main()