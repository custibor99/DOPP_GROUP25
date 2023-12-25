import pandas as pd
import time 
from tqdm import tqdm
import requests
import urllib.parse

def main():
    key = input("Please enter your google maps api key:")
    cities = pd.read_csv("../data/airport_metadata.csv")["city"].unique()
    city_location_data = {
        "city": [],
        "lat": [],
        "lng": [],
    }
    for city in tqdm(cities):
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city}&key={key}"
        url_parsed = urllib.parse.quote(url, safe="://=?&")
        response = requests.get(url_parsed)
        lat = None
        long = None
        if response.status_code == 200:
            try:
                lat = response.json()["results"][0]["geometry"]["location"]["lat"]
                lng = response.json()["results"][0]["geometry"]["location"]["lng"]
            except:
                pass
        
        city_location_data["city"].append(city)
        city_location_data["lat"].append(lat)
        city_location_data["lng"].append(lng)
    
    pd.DataFrame(data=city_location_data).to_csv("../data/city_coordinates.csv", index=False)
if __name__ == "__main__":
    main()
