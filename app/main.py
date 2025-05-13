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
from interface.input_parser import Interface, Interface_administrator, Interface_batch
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
    # queryhandler = QueryBuilder()
    # table_name = "genres"
    # create_new_table = queryhandler.create_cid_table(table_name)
    # print(create_new_table)
    # dbhandler.execute_query(create_new_table)
    # table_name = "genres"
    # create_new_cid_table = queryhandler.create_cid_table(table_name)
    # print(create_new_cid_table)
    # dbhandler.execute_query(create_new_cid_table)


    
    # batch_handler
    # lon, lat, add = batch_handler.add_new_location(input_location)
    # print(lon)

    batch_handler = DatabasePreprocessing()
    location_counts = int(input())
    # print(location_counts)
    # for i in range(location_counts):
    #     location = batch_handler.add_new_location(input())
    #     print(location.batch_locations[i])
    #     batch_lon, batch_lat, batch_address = batch_handler.get_geocoding(location.batch_locations[i])
    id = uuid.uuid4()
    #     print(location_id)
    location_id = "d688319f-5ea8-4807-8af8-8e568bd27c87"
    genre = "historic_site"
    params = (
        location_id,  # id
        id,
        genre
    )
    sql_handler = QueryBuilder()
    query = sql_handler.insert_cid_datasets(genre)

    #     query = sql_handler.insert_parent_datasets("locations")
    dbhandler = DatabaseService()
    is_insert = dbhandler.execute_query(query, params)
    print(is_insert)
        




 


        

    




if __name__ == "__main__":
    main()
