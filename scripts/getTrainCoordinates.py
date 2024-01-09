import json
import os
import tqdm
import pandas as pd

def get_train_coordinates(json_filepath:str) -> pd.DataFrame:
    coordinates = {
        "id" : [],
        "lat" : [],
        "lng" : [],
    }

    for file in tqdm.tqdm(os.listdir(json_filepath)):
        if file.endswith(".json"):
            with open(json_filepath+file, "r") as file:
                out = file.read()
                obj = json.loads(out)
                
                lat = list(str(obj["origin"]["longitudeE7"]))
                lat.insert(2,".")
                lat = "".join(lat)
            
                lng = list(str(obj["origin"]["latitudeE7"]))
                lng.insert(2,".")
                lng = "".join(lng)
            coordinates["id"].append(file.name.split("/")[-1].split("_")[0])
            coordinates["lat"].append(lat)
            coordinates["lng"].append(lng)
    res = pd.DataFrame(data=coordinates)    
    res = res.drop_duplicates()
    return res

def main():
    train_coordinates = get_train_coordinates("../data/json_data/")
    train_coordinates.to_csv("../data/station_coordinates.csv", index=False)

if __name__ == "__main__":
    main()