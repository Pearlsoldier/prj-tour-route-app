# サーバーのメインファイル（例：app.py）にも同様のパス設定を追加
import sys
import os
from rich.console import Console
import pprint
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import Union
from fastapi import FastAPI
from location.management import LocationManager

from geocoding.geocoding import Geocoding, ReverseGeocoding
from location.locations import Location
from interface.input_parser import (
    Interface,
    InterfaceAdministrator,
    InterfaceBatch,
    CidInterfaceBatch,
)

from DB.database import DatabaseService
from sql.postgresql import QueryBuilder
from batch.preprocessing import DatabasePreprocessing
from metrics_module.metrics_Interface import (
    DistanceLocationDataSets,
    DistanceMetrics,
    SpeedMetrics,
    TimeMetrics
)
from metrics_module.calculation import calculate_locations_distance

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
    # tky_tow = Location("東京タワー")
    # tky_sta = Location("東京駅")
    # location_handler = DistanceLocationDataSets(start_location=tky_sta, end_location=tky_tow)
    # print(location_handler.start_location)
    # result = calculate_locations_distance(location_handler.start_location, location_handler.end_location)
    # print(result)
    walk = SpeedMetrics(700)
    transit = TimeMetrics(20)
    distance = walk.speed * transit.time
    print(distance)
    within_range = DistanceMetrics(distance)
    print(within_range.distance)
    print(type(within_range.distance))



if __name__ == "__main__":
    main()
