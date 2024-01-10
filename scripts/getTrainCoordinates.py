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
                
                lat1 = list(str(obj["origin"]["longitudeE7"]))
                lat1.insert(2,".")
                lat1 = "".join(lat1)
            
                lng1 = list(str(obj["origin"]["latitudeE7"]))
                lng1.insert(2,".")
                lng1 = "".join(lng1)

                lat2 = list(str(obj["destination"]["longitudeE7"]))
                lat2.insert(2,".")
                lat2 = "".join(lat2)
            
                lng2 = list(str(obj["destination"]["latitudeE7"]))
                lng2.insert(2,".")
                lng2 = "".join(lng2)
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