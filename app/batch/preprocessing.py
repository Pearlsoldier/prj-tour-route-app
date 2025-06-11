from interface.input_parser import InterfaceBatch
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
        self.batch_locations = InterfaceBatch()

    def add_new_location(self, location):
        self.batch_locations.batch_locations.append(location)
        return self.batch_locations

    def get_geocoding(self, location):
        batch_coordinates = Geocoding().get_coordinate(location)
        batch_location = Location(batch_coordinates, location)
        batch_lat = batch_location.latitude.value
        batch_lon = batch_location.longitude.value

        batch_reverse_coding = ReverseGeocoding()
        batch_address = batch_reverse_coding.get_address(batch_lat, batch_lon)
        return batch_lon, batch_lat, batch_address

    def insert_location_datasets(self, id, location_name, address, longitude, latitude):
        batch_db = DatabaseService()
        is_batch = batch_db.add_value(id, location_name, address, longitude, latitude)
        return is_batch
    
    def insert_genre_datasets(self, location_id, id, genre):
        batch_db = DatabaseService()
        is_batch = batch_db.add_value(location_id, id, genre)
        return is_batch


class CidDatabasePreprocessing():
    """

    """

    def __init__(self):
        self.batch_locations = InterfaceBatch()
