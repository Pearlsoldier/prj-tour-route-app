from locations import Location
from geocoding import Geocoding


class LocationManager:
    def __init__(self, place_name):
        geo_place = Geocoding(place_name)
        coordinates = geo_place.get_coordinate()
        lat = coordinates[0]
        lon = coordinates[1]
        self.locations_data = Location(lat, lon, place_name)

