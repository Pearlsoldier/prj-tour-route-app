from location.locations import Location
from location.geocoding import Geocoding
from location.mapping import Mapping


class LocationManager:
    """
    施設名を引数に経度、緯度、施設名のインスタンスを扱う
    """
    def __init__(self, place_name):
        locator = Location(place_name)
        self.locations_data = locator
    
class MappingManager:
    def __init__(self, location):
        location_map = Mapping(location)
        self.initmap = location_map.map
        
