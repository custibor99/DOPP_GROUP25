import math
import pandas as pd
import networkx as nx
from tqdm import tqdm
import os

# To consider:
# Aircraft speed varies greatly by model, flight distance and airline (fuel cost)
# Incorporate this data?
# https://www.researchgate.net/figure/Relation-between-flight-distance-and-speed-for-intra-European-flights-2018_fig2_338595902

# Prevailing winds (global, seasonal trends). Used to calculate true airspeed,
# not sure of significance at short distance flights

# Outbound/ inbound flights within Europe might have up to 25 minutes difference.
# Calculations are still a *little* off.


# Average plane speed for short distance commercial flights (in m/h)
avg_speed = 550000

# Average boarding time (in minutes)
boarding_time = 30

# Average time to leave the plane (in minutes)
alight_time = 15


# https://www.movable-type.co.uk/scripts/latlong.html
# φ/λ = latitude/longitude in radians
# Haversine a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
# formula:	c = 2 ⋅ atan2( √a, √(1−a) )
#           d = earth_radius ⋅ c
def calculate_distance(lat1, lon1, lat2, lon2) -> int:
    earth_radius = 6371e3
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (math.sin(delta_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(delta_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return round(earth_radius * c)


def calculate_duration(distance) -> int:
    flight_duration = distance / avg_speed
    full_duration = flight_duration + boarding_time + alight_time
    return round(full_duration * 60 * 60)


def main():
    airport_metadata = pd.read_csv('../data/airport_metadata.csv')
    airport_coordinates = pd.read_csv('../data/airport_coordinates.csv')
    airport_data = airport_metadata.merge(airport_coordinates, left_on="IATA airport code", right_on="iata_code")

    #if os.path.isfile("../data/flight_network.gml"):
    #    G = nx.read_gml("../data/flight_network.gml")
    #else:
    G = nx.Graph()

    for idx_place, place in tqdm(airport_data.iterrows()):
        for idx_dest, dest in airport_data.iterrows():
            if G.has_edge(place['city'], dest['city']):
                continue

            distance = calculate_distance(place['lat'], place['lng'], dest['lat'], dest['lng'])
            duration = calculate_duration(distance)
            G.add_edge(place['city'], dest['city'], distance=distance, duration=duration)

    nx.write_gml(G, "../data/flight_network.gml")


if __name__ == "__main__":
    main()

