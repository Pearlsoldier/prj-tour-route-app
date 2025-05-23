from dataclasses import dataclass
from location.locations import Location

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

    distance: float


@dataclass
class SpeedMetrics:
    """
    きはじの速さを扱うクラス
    """

    speed: int


@dataclass
class TimeMetrics:
    """
    きはじの時間を扱うクラス
    """

    time: int
