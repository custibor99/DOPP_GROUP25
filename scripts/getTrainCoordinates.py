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

    for file_name in tqdm.tqdm(os.listdir(json_filepath)):
        if file_name.endswith(".json"):
            
            with open(json_filepath+file_name, "r") as file:
                if "3190261" in file.name:
                    print(file.name)
                out = file.read()
                obj = json.loads(out)
                
                lng1 = float(obj["origin"]["longitudeE7"]) / 10**7
                lat1 = float(obj["origin"]["latitudeE7"]) / 10**7
                lng2 = float(obj["destination"]["longitudeE7"]) / 10**7
                lat2 = float(obj["destination"]["latitudeE7"]) / 10**7
                
                coordinates["id"].append(file.name.split("/")[-1].split("_")[0])
                coordinates["id"].append(file.name.split("/")[-1].split("_")[2].split(".")[0])
    
                coordinates["lat"].append(lat1)
                coordinates["lat"].append(lat2)
    
                coordinates["lng"].append(lng1)
                coordinates["lng"].append(lng2)

    res = pd.DataFrame(data=coordinates)    
    res = res.drop_duplicates()
    return res

def main():
    train_coordinates = get_train_coordinates("../data/json_data/")
    train_coordinates.to_csv("../data/station_coordinates.csv", index=False)

if __name__ == "__main__":
    main()