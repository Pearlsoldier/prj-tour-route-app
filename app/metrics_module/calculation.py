from metrics_module.metrics_Interface import DistanceLocationDataSets
from metrics_module.metrics_Interface import DistanceMetrics
from metrics_module.metrics_Interface import SpeedMetrics
from metrics_module.metrics_Interface import TimeMetrics


from location.locations import Location
from geocoding.geocoding import Distance


import requests


def calc_locations_distance(start_location: str, end_location: str) -> float:
    distance_handler = Distance(
        start_location=start_location, end_location=end_location
    )
    return distance_handler._distance


def calc_distance(speed: int, time: int) -> int:
    return speed * time


def calc_speed(time: int, distance: int) -> int:
    return distance // time


def calc_time(distance: int, speed: int) -> int:
    return distance // speed
