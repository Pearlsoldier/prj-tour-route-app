from urllib.parse import urlparse, parse_qs

# サーバーのメインファイル（例：app.py）にも同様のパス設定を追加
import sys
import os
from rich.console import Console
import pprint
import uuid
import pandas

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import Union
from fastapi import FastAPI
from location.management import LocationManager, MappingManager

from app.mapping.mapgenerator import MapGenerator
from app.mapping.mapplotter import MapPlotter


from geocoding.geocoding import Geocoding, ReverseGeocoding
from location.locations import Location, AccessibleLocation
from interface.input_parser import (
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

import os
from dotenv import load_dotenv
from pydantic import BaseModel


from google import genai
from google.genai import types


def main():

    url = "https://api.example.com/v1/places/nearby?q=東京駅&radius=500&category=cafe"
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    if "q" not in params or not params["q"][0]:
        raise ValueError("必須パラメータ'q'が指定されていません")

    result = {
        "start_position": params["q"][0],
        "radius": int(params["radius"][0]) if "radius" in params else 1000,
        "category": params["category"][0] if "category" in params else None,
        "limit": int(params["limit"][0]) if "limit" in params else 20,
    }
    start_position = result["start_position"]

    load_dotenv()

    def is_accessible(locations_distance: float, radius: int):
        return locations_distance < radius

    # 移動手段と所有時間から移動可能圏内を導く
    sql_handler = QueryBuilder()
    locations_tabale_query = sql_handler.get_locations_table()
    db_handler = DatabaseService()
    locations_table = db_handler.execute_query_fetch(locations_tabale_query)
    # print(f"locations_table: {locations_table}")
    within_range_locations = []
    start_position = Location(start_position)
    start_location = start_position.location

    for i in range(len(locations_table)):
        locations_name = locations_table[i][1]
        locations_id = locations_table[i][0]
        end_location = locations_name

        if start_location == end_location:
            # print(f"end : {end_location}")
            continue
        get_genres_query = sql_handler.get_genres(end_location)
        genres_table = db_handler.execute_query_fetch(
            get_genres_query, params=(locations_table[i][0],)
        )
        locations_distance = LocationsDistance(
            start_location=start_location, end_location=end_location
        )
        distance = locations_distance.locations_distance
        if is_accessible(locations_distance=distance, radius=result["radius"]):
            end_location_handler = Location(end_location)
            locations_name = genres_table[0][1]

            location_and_genres = AccessibleLocation(
                end_location_handler.location, end_location_handler.address
            )
    return {location_and_genres.locations_name, location_and_genres.adress}


if __name__ == "__main__":
    main()
