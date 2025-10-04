from geocoding.geocoding import Geocoding, ReverseGeocoding
from location.locations import Location, Coordinate
from DB.database import DatabaseService


class RegistrationInformation:
    """
    データベースに登録するためのオブジェクト
    """

    def __init__(self, location):
        self._location = Location(location)

    def get_geocoding(self):

        coordinates = Geocoding().get_coordinate(self._location.location)
        lat = coordinates[0]
        lon = coordinates[1]

        reverse_coding = ReverseGeocoding()
        address = reverse_coding.get_address(lat, lon)
        return address, lon, lat

    def insert_location_config(self, id, location_name, address, longitude, latitude):
        db = DatabaseService()
        is_batch = db.add_value(id, location_name, address, longitude, latitude)
        return is_batch

    def insert_genre_datasets(self, location_id, id, genre):
        db = DatabaseService()
        is_batch = db.add_value(location_id, id, genre)
        return is_batch


