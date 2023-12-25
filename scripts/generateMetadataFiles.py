from countryinfo import CountryInfo
import pandas as pd
import time

def log_pipeline_steps(func):
    def wrapper(df: pd.DataFrame) -> pd.DataFrame:
        start = time.time()
        res =  func(df)
        end = time.time()
        print(f"{func.__name__} took {end-start} seconds. input shape: {df.shape}, output shape: {res.shape}")
        return res
    return wrapper

@log_pipeline_steps
def start_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    copy = df.copy()
    return copy

def read_country_data(filename: str) -> pd.DataFrame:  
    airport_data = pd.read_csv(filename)
    country_names = airport_data["Country"].unique()
    country_data = {"name": country_names}
    return pd.DataFrame(data=country_data)

@log_pipeline_steps
def append_country_code(df: pd.DataFrame) -> pd.DataFrame:
    country_name = None
    country_codes = []
    for name in df["name"]:
        country_code = None
        try:
            country = CountryInfo(name)
            country_code = country.iso()["alpha3"]
        except:
            pass
        
        country_codes.append(country_code)
    
    df["code"] = country_codes
    return df

@log_pipeline_steps
def fill_missing_country_codes(df: pd.DataFrame) -> pd.DataFrame:
    mappings = {
        "Kosovo": "XKK",
        "Montenegro" : "MNE",
        "North Macedonia": "MKD",
    }
    df["code"] = df.apply(lambda x: mappings[x["name"]] if x["code"] is None else x["code"], axis=1)
    return df

@log_pipeline_steps
def get_neighbor_countries(df: pd.DataFrame) -> pd.DataFrame:
    neighbors = []
    unique_codes = df["code"].unique()
    for name in df["name"]:
        neighbor = None
        try:
            country = CountryInfo(name)
            neighbor = country.borders()
            neighbor = [code for code in neighbor if code in unique_codes]
            neighbor = ",".join(neighbor)
        except:
            pass
        
        neighbors.append(neighbor)
    
    df["neighbors"] = neighbors
    return df
    
@log_pipeline_steps
def fill_missing_neighbors(df: pd.DataFrame) -> pd.DataFrame:
    mappings = {
        "Kosovo": "MNE,SRB,MKD,ALB",
        "Montenegro" : "XKK,ALB,HRV,SRB,BIH",
        "North Macedonia": "ALB,XKK,SRB,GRC,BGR",
        "United Kingdom": "IRL,FRA",
        "France": "BEL,DEU,ITA,LUX,ESP,CHE,GBR",
        "Sweden": "FIN,NOR,DNK",
        "Cyprus": "",
    }
    df["neighbors"] = df.apply(lambda x: mappings[x["name"]] if (x["name"] in mappings.keys()) else x["neighbors"], axis=1)
    return df

@log_pipeline_steps
def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    mapping = {
        "name": "Country",
        "code": "iso_country_code"
    }
    return df.rename(columns=mapping)

def read_airport_data(filename: str) -> pd.DataFrame:  
    airport_data = pd.read_csv(filename)
    airport_data["city"] = airport_data["Airport"].str.replace("Airport", "")
    airport_data["city"] = airport_data["city"].str.replace(r"London [a-zA-Z ]*", "London", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Stockholm [a-zA-Z ]*", "Stockholm", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Kiev [a-zA-Z ]*", "Kiev", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Milan [a-zA-Z ]*", "Milan", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Paris [a-zA-Z ]*", "Paris", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Cologne [a-zA-Z ]*", "Cologne", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Frankfurt [a-zA-Z ]*", "Frankfurt", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Rome [a-zA-Z ]*", "Rome", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Rijeka [a-zA-Z ]*", "Rijeka", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Rome [a-zA-Z ]*", "Rome", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Ostend [a-zA-Z ]*", "Ostend", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Lyon[ -a-zA-Z ]*", "Lyon", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Yerevan [a-zA-Z ]*", "Zvartnots", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Figari [a-zA-Z ]*", "Figari", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Lesvos [a-zA-Z ]*", "Lesvos", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Catania [a-zA-Z ]*", "Catania", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Leeds [a-zA-Z ]*", "Leeds", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Brest [a-zA-Z ]*", "Brest", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Karlsruhe [a-zA-Z ]*", "Karlsruhe", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Frankfurt-[a-zA-Z ]*", "Frankfurt", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Leipzig [a-zA-Z ]*", "Leipzig", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Paderborn [a-zA-Z ]*", "Paderborn", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Rennes [a-zA-Z ]*", "Rennes", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Toulouse [a-zA-Z ]*", "Toulouse", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Toulon-[a-zA-Z ]*", "Toulon", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Ireland [a-zA-Z ]*", "Knock", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Olbia [a-zA-Z ]*", "Olbia", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Nursultan [a-zA-Z ]*", "Astana", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Amsterdam [a-zA-Z ]*", "Amsterdam", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Groningen [a-zA-Z ]*", "Groningen", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Maastricht [a-zA-Z ]*", "Maastricht", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Rotterdam [a-zA-Z ]*", "Rotterdam", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Moscow [a-zA-Z ]*", "Moscow", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Belgrade [a-zA-Z ]*", "Belgrade", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Tenerife [a-zA-Z ]*", "Tenerife", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Basel [a-zA-Z ]*", "Basel", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Ankara [a-zA-Z ]*", "Ankara", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Izmir [a-zA-Z ]*", "Izmir", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Glasgow [a-zA-Z ]*", "Glasgow", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Belfast [a-zA-Z ]*", "Belfast", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Madrid [a-zA-Z ]*", "Madrid", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Istanbul [a-zA-Z ]*", "Istanbul", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Warsaw [a-zA-Z ]*", "Warsaw", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Granada-[a-zA-Z ]*", "Granada", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Bucharest [a-zA-Z ]*", "Bucharest", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Milas-[a-zA-Z ]*", "Milas", regex=True)
    airport_data["city"] = airport_data["city"].str.replace("Allgäu  Memmingen", "Memmingen")
    airport_data["city"] = airport_data["city"].str.replace(r"Karlsruhe-[a-zA-Z ]*", "Karlsruhe", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Münster [a-zA-Z ]*", "Münster", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Gothenburg [a-zA-Z ]*", "Gothenburg", regex=True)
    airport_data["city"] = airport_data["city"].str.replace("Lyonint Exupéry", "Lyon-St")
    airport_data["city"] = airport_data["city"].str.replace(r"Réunion [a-zA-Z ]*", "Réunion", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Sandefjord [a-zA-Z ]*", "Sandefjord", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Saint [a-zA-Z ]*", "Saint Petersburg", regex=True)
    airport_data["city"] = airport_data["city"].str.replace(r"Sandefjord [a-zA-Z ]*", "Sandefjord", regex=True)
    airport_data["city"] = airport_data["city"].str.strip()
    return airport_data

def main():
    country_data = read_country_data("../data/airport codes eu.csv")
    country_data = (
    country_data
     .pipe(start_pipeline)
     .pipe(append_country_code)
     .pipe(fill_missing_country_codes)
     .pipe(get_neighbor_countries)
     .pipe(fill_missing_neighbors)
     .pipe(rename_columns)
    )
    country_data.to_csv("../data/country_metadata.csv", index=False)
    print("Done. Generated file data/country_metadata.csv")
    airport_data = read_airport_data("../data/airport codes eu.csv")
    airport_data.to_csv("../data/airport_metadata.csv", index=False)
    print("Done. Generated file data/airport_metadata.csv")

if __name__ == "__main__":
    main()
