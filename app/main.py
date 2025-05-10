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
from DB.database import DatabaseService
from SQL.postgresql import QueryBuilder
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
    # """
    # DB操作の使用例
    # 新しいテーブルを作成
    # """
    # dbhandler = DatabaseService()
    # queryhandler = QueryBuilder()
    # table_name = "hogehoge"
    # create_new_table = queryhandler.create_table(table_name)
    # print(create_new_table)
    # dbhandler.execute_query(create_new_table)


if __name__ == "__main__":
    main()
