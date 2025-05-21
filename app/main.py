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

from metrics_module.metrics_Interface import MetricsDataBase, LocationMetricsDataSets

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
    metrics_handler = LocationMetricsDataSets(
        start_location="東京駅", end_location="東京タワー"
    )
    start = metrics_handler.start_location
    print(start)


if __name__ == "__main__":
    main()
