from dataclasses import dataclass
from location.locations import Location

from transport.transport import Walk
from transport.transport import Bicycle
from transport.transport import Car

from transittime.timerequired import TimeRequired


@dataclass
class DistanceLocationDataSets:
    """
    ２地点間の距離を扱うクラス
    """

    start_location: Location
    end_location: Location


@dataclass
class DistanceMetrics:
    """
    きはじの距離を扱うクラス
    """

    distance: int


@dataclass
class SpeedMetrics:
    """
    きはじの速さを扱うクラス
    """

    walk_speed: Walk.movement_speed
    Bicycle_speed: Bicycle.movement_speed
    car_speed: Car.movement_speed


@dataclass
class TimeMetrics:
    """
    きはじの時間を扱うクラス
    """

    time: TimeRequired
