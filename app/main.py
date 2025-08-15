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
from typing import List

from llm.prompts import system_prompt, user_prompt
from llm.interface import ClientBuilder, ChatInterface
from llm.config.config import Config


from google import genai
from google.genai import types


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
    trans_car = Car()
    within_tky_sta = WithinRange(trans_car.movement_speed, input["transit_time"])
    radius = within_tky_sta.within_range

    tky_sta = Location(start_location)
    start_map_instance = MapGenerator(
        tky_sta._location, tky_sta._latitude, tky_sta._longitude, zoom_start=15
    )
    mapping_tokyo_station = MapPlotter(start_map_instance.map)
    mapping_tokyo_station.plot_point(tky_sta)
    plot_tokyo_station = mapping_tokyo_station.plot_circle_mark(tky_sta, radius)
    #  start_map_instance.generate_map_from_plotter(plot_tokyo_station)

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
        distance = locations_distance.locations_distance
        if is_accessible(locations_distance=distance, within_range=radius):
            end_location_handler = Location(end_location)
            locations_name = genres_table[0][1]
            genres_1 = genres_table[0][2]
            genres_2 = genres_table[1][2]

            location_and_genres = AccessibleLocation(
                end_location_handler.location, genres_1, genres_2
            )
            # print(location_and_genres.locations_name)
            # print(location_and_genres.genres1)
            # print(location_and_genres.genres2)
            mapping_tokyo_station.plot_point(end_location_handler)
            within_range_locations.append(location_and_genres)
    start_map_instance.generate_map_from_plotter(mapping_tokyo_station)
    print(within_range_locations)

    is_continue_conversation = True
    chat = []
    while is_continue_conversation:
        user_input = input()
        location_data_sets = within_range_locations
        builder = ClientBuilder
        gemini_model = builder.set_up_model()
        gemini_contents = builder.create_contents(user_input=user_input)
        gemini_system_prompt = builder.create_system_instruction(
            location_datasets=location_data_sets
        )
        gemini_config = builder.create_config(
            gemini_system_instruction=gemini_system_prompt
        )

        gemini_chat = ChatInterface(
            model=gemini_model, config=gemini_config, contents=gemini_contents
        )
        chat = gemini_chat.start_chat()
        print(chat.parsed.response)
        print(chat.parsed.is_continue_conversation)


if __name__ == "__main__":
    main()
