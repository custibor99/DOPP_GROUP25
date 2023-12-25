import pandas as pd
import time 
from tqdm import tqdm
import requests
import urllib.parse


def main():
    airport_metadata = pd.read_csv("../data/airport_metadata.csv")
    chronotrains = airport_metadata[["Country", "city"]].copy()

    start = time.time()
    chrono_trains_codes = []
    data = {}
    
    for city in tqdm(airport_metadata["city"].unique()):
        res = None
        url = f"https://www.chronotrains.com/api/search/{city}"
        url_parsed = urllib.parse.quote(url, safe="://")
        response = requests.get(url_parsed)
        if response.status_code == 200:
            try:
                res = response.json()[0]["aliases"][0]
            except:
                pass
        chrono_trains_codes.append(res)
        time.sleep(0.5)
    
    data["chronotrain_id"] = chrono_trains_codes
    data["city"] = airport_metadata["city"].unique()
    chronotrains = pd.DataFrame(data=data).merge(airport_metadata, on="city")
    chronotrains.to_csv("../data/chronotrains.csv", index=False)
    
    end = time.time()
    print(f"Fetched all ids in {end-start} seconds")
    print(f"Created file data/chronotrains.csv")

if __name__ == "__main__":
    main()
