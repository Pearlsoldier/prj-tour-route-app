# サーバーのメインファイル（例：app.py）にも同様のパス設定を追加
import sys
import os
from rich.console import Console
import pprint
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import Union
from fastapi import FastAPI
from location.management import LocationManager, MappingManager

from mapping.mapping import Mapping

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

app = FastAPI()


@app.get("/location/{place_name}/")
def get_coordinates(place_name):
    try:
        locator = LocationManager(place_name)
        return locator.locations_data
    except Exception as e:
        return e


# @app.get("/map/{mapping}/")
# def mapping(place_name):
#     try:
#         map = MappingManager(place_name)
#         return map.initialized_map
#     except Exception as e:
#         return e


def main():

    def is_accessible(locations_distance: float, within_range: int):
        return locations_distance < within_range

    # 移動手段と所有時間から移動可能圏内を導く
    sql_handler = QueryBuilder()
    locations_tabale_query = sql_handler.get_locations_table()
    db_handler = DatabaseService()
    locations_table = db_handler.execute_query_fetch(locations_tabale_query)
    # print(f"locations_table: {locations_table}")
    # print(f"locations_table: {locations_table[0]}")
    within_range_locations = []

    input = {"location": "東京駅", "transport": "Car", "transit_time": 3}
    start_location = input["location"]
    tky_sta = Location(start_location)
    start_map = Mapping(
        tky_sta._location, tky_sta._latitude, tky_sta._longitude, zoom_start=15
    )

    start_map_tky_sta = start_map.plot_start_mark()
    able_tky_sta = start_map_tky_sta.plot_circle_mark()

    trans_car = Car()

    within_tky_sta = WithinRange(trans_car.movement_speed, input["transit_time"])
    radius = within_tky_sta.within_range
    print(radius)
    able_tky_sta = start_map_tky_sta.plot_circle_mark(with_in_range=radius)
    print(able_tky_sta.mapping())
    for i in range(len(locations_table)):
        locations_name = locations_table[i][1]
        locations_id = locations_table[i][0]
        end_location = locations_name

        if start_location == end_location:
            print(f"end : {end_location}")
            continue
        get_genres_query = sql_handler.get_genres(end_location)
        genres_table = db_handler.execute_query_fetch(
            get_genres_query, params=(locations_table[i][0],)
        )
        locations_distance = LocationsDistance(
            start_location=start_location, end_location=end_location
        )
        within_range = within_tky_sta.within_range
        distance = locations_distance.locations_distance
        if is_accessible(locations_distance=distance, within_range=within_range):
            locations_name = genres_table[0][1]
            genres_1 = genres_table[0][2]
            genres_2 = genres_table[1][2]

            location_and_genres = AccessibleLocation(locations_name, genres_1, genres_2)
            print(location_and_genres.locations_name)
            print(location_and_genres.genres1)
            print(location_and_genres.genres2)
            within_range_locations.append(location_and_genres)
            # accessibleLocation = AccessibleLocation()
            print(within_range_locations)


if __name__ == "__main__":
    main()
