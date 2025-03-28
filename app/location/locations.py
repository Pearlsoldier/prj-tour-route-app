from geocoding import Geocoding

class Location:
    def __init__(self, place_name: str):
        geocode = Geocoding(place_name)
        coordinates = geocode.get_coordinate()
        self.lat = coordinates[1]
        self.lon = coordinates[0]
        self.place_name = place_name

def main():
    locator = Location("東京駅")
    print(locator.lat)
    print(locator.lon)
    print(locator.place_name)

if __name__ == "__main__":
    main()
