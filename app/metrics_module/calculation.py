from metrics_module.metrics_Interface import DistanceLocationDataSets
from metrics_module.metrics_Interface import DistanceMetrics
from metrics_module.metrics_Interface import SpeedMetrics
from metrics_module.metrics_Interface import TimeMetrics


from location.locations import Location


import requests


def calc_locations_distance(start_location, end_location):
    OUTPUT_TYPE = "json"
    ELLIPSOID = "GRS80"
    lat1 = start_location.latitude
    lon1 = start_location.longitude
    lat2 = end_location.latitude
    lon2 = end_location.longitude
    cal_api = f"https://vldb.gsi.go.jp/sokuchi/surveycalc/surveycalc/bl2st_calc.pl?outputType={OUTPUT_TYPE}&ellipsoid={ELLIPSOID}&latitude1={lat1}&longitude1={lon1}&latitude2={lat2}&longitude2={lon2}"
    response = requests.get(cal_api)
    data = response.json()
    output = data["OutputData"]
    return output.get("geoLength")


def calc_distance(speed: int, time: int) -> int:
    return speed * time


def calc_speed(time: int, distance: int) -> int:
    return distance // time


def calc_time(distance: int, speed: int) -> int:
    return distance // speed
