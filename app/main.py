# サーバーのメインファイル（例：app.py）にも同様のパス設定を追加
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import Union
from fastapi import FastAPI
from location.management import LocationManager

from geocoding.geocoding import Geocoding
from location.locations import Location
from interface.input_parser import Interface
from calculation.distance_calculation import DistanceCalculator
from manager.manager import FacilityManager

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
    # # Interfaceクラスの使用テスト
    # interfaces = Interface(place=input(), transport=input(), transit_time=input(), )
    # print(f"input_place: {interfaces.place}")
    # print(f"input_transport: {interfaces.transport}")
    # print(f"input_transit_time: {interfaces.transit_time}")

    # # Geocodingクラスの使用例
    # geocoding_service = Geocoding()
    # geocoding = geocoding_service.get_coordinate(place=interfaces.place)
    # print(f"lan: {geocoding[0]}")   # [float, float]

    # # Locationクラスの使用例
    # tokyo_station = Location(geocoding=geocoding, place=interfaces.place)
    # print(tokyo_station.place)
    # print(tokyo_station.latitude)
    # print(tokyo_station.longitude)

    # tokyo_tower = Location(geocoding=geocoding, place="東京タワー")

    # # DistanceCalculatorクラスの使用例
    # distance = DistanceCalculator(tokyo_station, tokyo_tower)
    # result = distance.calculate
    # print(f"distance: {result}")

    # FacilityManagerクラスの使用例
    manager = FacilityManager()
    idgetter = manager.get_id
    idgetter()


if __name__ == "__main__":
    main()
