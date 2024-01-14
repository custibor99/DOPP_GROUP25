import generateNetworks 
import generateMetadataFiles
import getCityCoordinates
import getChronotrainIds
import getTrainDurations
import getTrainCoordinates
import getCarDurations
import getAirportCoordinates
import cleanTabularData
import combineGraphData
import getCityAirportStationDurations

def main():
    # Fetch data
    generateMetadataFiles.main()
    generateNetworks.main()
    getChronotrainIds.main()
    getTrainDurations.main()
    getTrainCoordinates.main()
    getCityCoordinates.main()
    getCarDurations.main()
    getAirportCoordinates.main() 

    # Clean and transform data
    cleanTabularData.main()
    getCityAirportStationDurations.main()
    combineGraphData.main()
    # Final cleanup

    

if __name__ == "__main__":
    print("Generating all data files")
    main()
    