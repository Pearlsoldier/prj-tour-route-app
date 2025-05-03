from interface.input_parser import Interface_batch
from geocoding.geocoding import Geocoding, ReverseGeocoding
from location.locations import Location, Coordinate
from DB.database import DatabaseService


class DatabasePreprocessing:
    """
    データベースへの接続→database.pyから接続
    入力に関しては、interfaceを利用する→新しくinterfaceにクラスを作成する
    __init__の時に、
    """

    def __init__(self):
        self.batch_place = Interface_batch()

    def add_places(self, place):
        self.batch_place.places.append(place)
        return self.batch_place

    def get_geocoding(self, place):
        batch_coordinates = Geocoding().get_coordinate(place)
        batch_location = Location(batch_coordinates, place)
        batch_lat = batch_location.latitude.value
        batch_lon = batch_location.longitude.value

        batch_reverse_coding = ReverseGeocoding()
        batch_address = batch_reverse_coding.get_address(batch_lat, batch_lon)
        return batch_lat, batch_lon, batch_address

    def add_database(self, place, address, latitude, longitude):
        batch_db = DatabaseService()
        is_batch = batch_db.add_value(place, address, latitude, longitude)
        return is_batch
