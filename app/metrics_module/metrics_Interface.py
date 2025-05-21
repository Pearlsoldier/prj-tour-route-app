from dataclasses import dataclass
from location.locations import Location


class MetricsDataBase:
    def __init__(self):
        pass


@dataclass
class DistanceLocationDataSets(MetricsDataBase):
    """
    ２地点間の距離を扱うクラス
    """

    start_location: str
    end_location: str


@dataclass
class DistanceMetrics(MetricsDataBase):
    """
    きはじの距離を扱うクラス
    """

    distance: float


@dataclass
class SpeedMetrics(MetricsDataBase):
    """
    きはじの速さを扱うクラス
    """

    speed: int


@dataclass
class TimeMetrics(MetricsDataBase):
    """
    きはじの時間を扱うクラス
    """

    time: int
