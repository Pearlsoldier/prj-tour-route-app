# サーバーのメインファイル（例：app.py）にも同様のパス設定を追加
import sys
import os
from rich.console import Console
import pprint

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import Union
from fastapi import FastAPI
from location.management import LocationManager

from geocoding.geocoding import Geocoding, ReverseGeocoding
from location.locations import Location
from interface.input_parser import Interface, Interface_administrator, Interface_batch
from calculation.distance_calculation import DistanceCalculator
from DB.database import PostgresCredentials, PostgresClient, DatabaseService
from batch.preprocessing import DatabasePreprocessing

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
#     print(f"入力したい施設数の数を入力してください: x箇所")
#     n = int(input())
#     print(f"入力したい施設数の数: {n}箇所")
#     demo = DatabasePreprocessing()

#     for i in range(n):
#         batch_place = demo.add_places(input())
#         batch_latitude, batch_longitude, batch_address = demo.get_geocoding(
#             batch_place.places[i]
#         )
#         is_demo = demo.add_database(
#             batch_place.places[i], batch_address, batch_latitude, batch_longitude
#         )
#         print(is_demo)
    addtable = DatabaseService()
    is_add_tabel = addtable.add_table()
    print(is_add_tabel)



if __name__ == "__main__":
    main()
