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
from calculation.distance_calculation import DistanceCalculator
from DB.database import DatabaseService
from sql.postgresql import QueryBuilder
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
    # table_name = "genres"
    # print("登録件数を入力してください")
    # batch_counts = int(input())
    # print(batch_counts)
    # sql_handler = QueryBuilder()
    # database_handler = DatabaseService()
    # for i in range(batch_counts):
    #     genres_id = uuid.uuid4()
    #     print("対象施設を入力してください。locationsテーブルにあるものに限られます。")
    #     location_name = input()
    #     query = sql_handler.get_location_id()
    #     get_uuid = database_handler.execute_query_fetch(query, (location_name,))
    #     batched_loction = get_uuid[0][0]
    #     print("ジャンルを入力してください")
    #     genre_name = input()
    #     cid_data_sets = Cid_Interface_batch(
    #         location=location_name,
    #         genre_name=genre_name,
    #         location_id=batched_loction,
    #         id=genres_id,
    #     )
    #     batched_query = sql_handler.insert_cid_datasets(table_name)
    #     params = (batched_loction, genres_id, genre_name)
    #     dbhandler.execute_query(batched_query, params)
    print("開始地点を入力してください。")
    location = input()
    print("移動手段を入力してください。")
    transport = input()
    print("所要時間を入力してください。")
    transit_time = input()
    candidate_location = Interface(location, transport, transit_time)
    hoge = get_coordinates(candidate_location.location)
    print(hoge)



if __name__ == "__main__":
    main()
