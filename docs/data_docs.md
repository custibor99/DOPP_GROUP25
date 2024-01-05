# Data documentation
## Description
This file contains description of all of the data files/sources used in the project. All of the data files can be found on [google drive](https://drive.google.com/drive/folders/1z65-V_g7631HaKvFRhrFEAztKkKnKc_s?usp=drive_link) or can be generated manually with the provided scripts.
## Data Sources
The folowing data sources have been used in the project:
- [List of largest european airports](https://airmundo.com/en/blog/airport-codes-european-airports/) according to AirMundo travel agency.
- [Pythons countryinfo package](https://github.com/porimol/countryinfo) for getting neighborings of european countries.
- [Chronotrains API](https://www.chronotrains.com/en) was used for obtaining train travel times between different cities
- [Google Maps Geocode API](https://developers.google.com/maps/documentation/geocoding/overview) were used for obtaining latitude and longitude coordinates of cities
- [Google maps distance matrix api](https://developers.google.com/maps/documentation/distance-matrix/overview) used for obtaining driving distances and durations between cities.

## Tabular files

### Airport codes eu.csv
Contains data about major european airports.

| Variable  | Description |
| ------------- | ------------- |
| Airport  | name of the airport  |
| Country  | country of airport  |
| IATA Airport code  | IATA code  |
| ICAO Airport code  | ICAO code  |

### country_metadata.csv
Contains metadata about the countries of our airports.

| Variable  | Description |
| ------------- | ------------- |
| Country  | name of the country  |
| ISO country code  | 3 letter ISO code of country  |
| neighbors  | coma seperated string of ISO codes of neighboring countries  |


### airport_metadata.csv
Similar data as **Airport codes eu.csv**. Additionaly contains a city column, which list the city or nearest city of the airport.

### chronotrains.csv
Contains data similar to **airport_metadata.csv**. Additionaly contains a id column for with the (chronotrains Api)[https://www.chronotrains.com/en] id.

### city_coordinates.csv
Contains city latitude and longitude obtained from [Google Maps Geocode API](https://developers.google.com/maps/documentation/geocoding/overview)
| Variable  | Description |
| ------------- | ------------- |
| City  | Name of city  |
| lat  | Latitude  |
| lng  | Longitude  |


### airport_coordinates.csv
Contains city latitude and longitude obtained from [Google Maps Geocode API](https://developers.google.com/maps/documentation/geocoding/overview)
| Variable  | Description |
| ------------- | ------------- |
| iata_code  | AIrport iata code  |
| lat  | Latitude  |
| lng  | Longitude  |

## Network files
Network files are saved in the [.gml](https://networkx.org/documentation/stable/reference/readwrite/gml.html) file format developed by the creators of the [networkx](https://networkx.org/documentation/stable/index.html) python library. 

### Country_network.gml
Contains the network structure of european countries. Countries are connected to their neighbors. 

### City_train_network.gml
Contains a network of cities. Cities are connected if they are in the same country or neighboring country. This is a simplification of the actuall train network. Some trains that travel from country A to country C trough country B
may not travel trough any of the Citys that we defined for country B. This has been done to decrease the ammount of [API](https://www.chronotrains.com/en) calls as each one takes a few seconds to complete. This alowed us to reduce the number of api cals from around 50000 to 4000. It only contains cities with valid chronotain ids.

### City_train_network_duration.gml
Contains the same structure as **City_train_network.gml** except that it has weighted nodes. The nodes are weighted based on the travel duration from the [Chronotrain Api](https://www.chronotrains.com/en). If is no train connection between two cities, then the value 99999 is used. It only contains cities with valid chronotain ids.

### City_car_network.gml
A netowrk containing all cities from the **chronotrains.csv** file that have a valid id. The constructed graphs should be fully connected. Each edge has two attributes; distance (meters) and duration (seconds). If a edge does not exist, there exist no connection between the locations according to the google maps api. 




