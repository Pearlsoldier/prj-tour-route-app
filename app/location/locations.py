from dataclasses import dataclass


@dataclass
class Coordinate:
    value: float
    type: str  # "latitude" または "longitude"

    def __str__(self):
        return str(self.value)


class Location:
    def __init__(self, geocoding: list[float], place: str) -> None:
        """
        Locationオブジェクトを初期化します
        Args:
            geocoding: [経度, 緯度]の形式の座標リスト
            place: 場所の名称
        longitude: 経度
        latitude: 緯度
        """
        self._longitude = Coordinate(geocoding[0], "longitude")
        self._latitude = Coordinate(geocoding[1], "latitude")
        self._place = place

    @property
    def latitude(self) -> Coordinate:
        return self._latitude

    @property
    def longitude(self) -> Coordinate:
        return self._longitude

    @property
    def place(self) -> str:
        return self._place
