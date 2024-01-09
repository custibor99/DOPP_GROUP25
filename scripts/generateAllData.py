import generateNetworks 
import generateMetadataFiles
import getCityCoordinates
import getChronotrainIds
import getTrainDurations
import getTrainCoordinates
import getCarDurations
import getAirportCoordinates
import cleanTabularData

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

    # Final cleanup
    

if __name__ == "__main__":
    print("Generating all data files")
    main()
    