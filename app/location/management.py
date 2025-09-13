import sys
import os

# appディレクトリをsys.pathに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# locationモジュールから直接インポート
from location.locations import Location
from geocoding.geocoding import Geocoding
from app.mapping.mapgenerator import MapGenerator


class LocationManager:
    # 以下のコード
    """
    施設名を引数に経度、緯度、施設名のインスタンスを扱う
    """

    def __init__(self, place_name):
        locator = Location(place_name)
        self.locations_data = locator
        self.lat = self.locations_data.lat
        self.lon = self.locations_data.lon
        self.place_name = self.locations_data.place_name


class MappingManager:
    def __init__(self, place_name, lat, lon):
        location_map = Mapping(place_name, lat, lon)
        self.initialized_map = location_map.map


def main():
    init = LocationManager("厳島神社")
    print(init.lat)
    mapping_location = MappingManager("厳島神社")
    print(mapping_location.initialized_map)


if __name__ == "__main__":
    main()
