import pandas as pd

def get_clean_airport_data(coordinates_filename:str, metadata_filename:str) -> pd.DataFrame:
    airport_coordinates = pd.read_csv(coordinates_filename)
    airport_metadata = pd.read_csv(metadata_filename)
    airport_data = airport_metadata.merge(airport_coordinates, left_on="IATA airport code", right_on="iata_code")
    airport_data = airport_data.drop(columns = ["IATA airport code"])
    airport_data = airport_data.rename(columns = {"ICAO airport code": "icao_code"})
    airport_data = airport_data.dropna()
    return airport_data

def get_clean_city_data(coordinates_file:str) -> pd.DataFrame:
    city_data = pd.read_csv(coordinates_file)
    city_data = city_data.dropna()
    return city_data

def get_clean_country_data(metadata_file:str) -> pd.DataFrame: 
    country_data = pd.read_csv(metadata_file)
    country_data = country_data.drop(columns=["neighbors"])
    return country_data.dropna()


def get_train_data_clean(train_filename:str, coordinates_filename:str)->pd.DataFrame:
    train_data = pd.read_csv(train_filename)
    train_data = train_data.dropna()
    train_data = train_data.drop(columns = ["Airport", "Country", "IATA airport code", "ICAO airport code"])
    train_coordinates = pd.read_csv(coordinates_filename)
    train_data = train_data.merge(train_coordinates, left_on="chronotrain_id", right_on="id")
    train_data = train_data.rename(columns={"lat":"train_station_lat", "lng":"train_station_lng"})
    train_data = train_data.drop(columns="id")
    return train_data

def join_data(airport_data: pd.DataFrame, country_data: pd.DataFrame, train_data:pd.DataFrame, city_data = pd.DataFrame) -> pd.DataFrame:
    merged = airport_data.merge(country_data)
    merged = merged.rename(columns = {"lat": "airport_lat", "lng":"airport_lng"})
    merged = merged.merge(train_data)
    merged = merged.merge(city_data)
    merged = merged.rename(columns = {"lat":"city_lat", "lng":"city_lng"})
    return merged


def main():
    airport_data = get_clean_airport_data("../data/airport_coordinates.csv", "../data/airport_metadata.csv")
    airport_data.to_csv("../data/clean/airport_data.csv", index=False)
    
    city_data = get_clean_city_data("../data/city_coordinates.csv")
    city_data.to_csv("../data/clean/city_data.csv", index=False)
    
    country_data = get_clean_country_data("../data/country_metadata.csv")
    country_data.to_csv("../data/clean/country_data.csv", index=False)
    
    train_data = get_train_data_clean("../data/chronotrains.csv", "../data/station_coordinates.csv")
    train_data.to_csv("../data/clean/station_data.csv", index=False)
    
    merged = join_data(airport_data, country_data, train_data, city_data)
    merged.to_csv("../data/clean/all_data.csv", index=False)

if __name__ == "__main__":
    print("Cleaning data")
    main()
