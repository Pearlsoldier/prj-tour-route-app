from metrics_module.calculation import calc_locations_distance
from metrics_module.calculation import calc_distance
from metrics_module.calculation import calc_speed
from metrics_module.calculation import calc_time


class LocationsDistance:
    """2地点の距離"""

    def __init__(self, start_location, end_location):
        self.locations_distance = calc_locations_distance(start_location, end_location)


class WithinRange:
    """所要時間と移動速度から割り出した圏内"""

    def __init__(self, speed: int, time: int) -> int:
        self.within_range = calc_distance(speed, time)


class Speed:
    """移動速度"""

    def __init__(self, time, distance):
        self.speed = calc_speed(time, distance)


class Time:
    """所有時間"""

    def __init__(self, distance, speed):
        self.time = calc_time(distance, speed)
