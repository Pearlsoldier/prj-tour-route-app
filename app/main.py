# サーバーのメインファイル（例：app.py）にも同様のパス設定を追加
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Union
from fastapi import FastAPI
from location.management import LocationManager, MappingManager

from location.geocoding import Geocoding
from location.locations import Location

app = FastAPI()


@app.get("/location/{place_name}/")
def get_coordinates(place_name):
    try:
        locator = LocationManager(place_name)
        return locator.locations_data
    except Exception as e:
        return e


@app.get("/map/{mapping}/")
def mapping(place_name):
    try:
        map = MappingManager(place_name)
        return map.initialized_map
    except Exception as e:
        return e


def main():
    # Geocodingクラスの使用例
    geocoding_service = Geocoding()
    geocoding = geocoding_service.get_coordinate(place="東京駅")
    print(geocoding) # [float, float]
    
    # Locationクラスの使用例
    tokyo_station = Location(geocoding=geocoding, place="東京駅")
    print(tokyo_station.place)
    print(tokyo_station.latitude)
    print(tokyo_station.longitude)
    

if __name__ == "__main__":
    main()
