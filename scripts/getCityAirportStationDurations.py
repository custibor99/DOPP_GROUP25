import pandas as pd
import numpy as np
import requests
import tqdm

def main():
    KEY = input("Enter google maps key: ")
    SEP1 = "%7C"
    SEP2 = "%2C"
    data = pd.read_csv("../data/clean/all_data.csv")
    coordinates = data[["city_lat", "city_lng", "airport_lat", "airport_lng", "train_station_lat", "train_station_lng"]]
    data["airport_duration"] = np.nan
    data["station_duration"] = np.nan

    for row in coordinates.iterrows():
        ind = row[0]
        val = row[1]
        city_lat = val["city_lat"]
        city_lng = val["city_lng"]
        airport_lat = val["airport_lat"]
        airport_lng = val["airport_lng"]
        train_lat = val["train_station_lat"]
        train_lng = val["train_station_lng"]
        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?destinations={airport_lat}%2C{airport_lng}%7C{train_lat}%2C{train_lng}&origins={city_lat}%2C{city_lng}&key={KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            airport_res = response.json()["rows"][0]["elements"][0]
            airport_distance = airport_res["duration"]["value"] / 60 if airport_res["status"] == "OK" else np.nan
            station_res = response.json()["rows"][0]["elements"][1]
            station_distance = station_res["duration"]["value"] / 60 if station_res["status"] == "OK" else np.nan
            data["airport_duration"].loc[ind] = airport_distance
            data["station_duration"].loc[ind] = station_distance
    data = data.dropna()
    data = data.drop_duplicates()
    data.to_csv("../data/clean/all_data.csv", index=False)
    
if __name__=="__main__":
    main()
