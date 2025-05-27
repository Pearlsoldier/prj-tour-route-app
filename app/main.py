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

from transport.transport import Walk
from transittime.timerequired import TimeRequired
from DB.database import DatabaseService
from sql.postgresql import QueryBuilder
from batch.preprocessing import DatabasePreprocessing

from metrics_module.metrics import LocationsDistance
from metrics_module.metrics import Speed
from metrics_module.metrics import WithinRange
from metrics_module.metrics import Time

from metrics_module.metrics_Interface import DistanceLocationDataSets
from metrics_module.metrics_Interface import DistanceMetrics

from transport.transport import Car

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
    # 移動手段と所有時間から移動可能圏内を導く
    input_handler = Interface(location="東京駅", transport="Car", transit_time=30)
    print(input_handler.transit_time)
    distance_locations_handler = DistanceLocationDataSets
    trans_car = Car()

    within_tky_sta = WithinRange(trans_car.movement_speed, input_handler.transit_time)
    print(within_tky_sta.within_range)



    # sql_handler = QueryBuilder()
    # locations_query = sql_handler.get_locations_table() 
    # db_handler = DatabaseService()
    # locations_table = db_handler.execute_query_fetch(locations_query)
    # locations_table




if __name__ == "__main__":
    main()
