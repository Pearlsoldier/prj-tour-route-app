from dataclasses import dataclass
from geocoding.geocoding import Geocoding, ReverseGeocoding


@dataclass
class Coordinate:
    value: float
    type: str  # "latitude" または "longitude"

    def __float__(self):
        return float(self.value)


class Location:
    """
    Locationオブジェクトを初期化します
    Args:
        geocoding: [経度, 緯度]の形式の座標リスト
        place: 場所の名称
    longitude: 経度
    latitude: 緯度
    """

    def __init__(self, location: str) -> None:
        self._location = location
        geocoding = Geocoding()
        self._cordinates = geocoding.get_coordinate(location)
        self._longitude = self._cordinates[0]
        self._latitude = self._cordinates[1]
        reversegeocoding = ReverseGeocoding()
        self._address = reversegeocoding.get_address(
            self._cordinates[0], self._cordinates[1]
        )

    @property
    def cordinates(self):
        return self._cordinates

    @property
    def latitude(self) -> Coordinate:
        return self._latitude

    @property
    def longitude(self) -> Coordinate:
        return self._longitude

    @property
    def location(self) -> str:
        return self._location

    @property
    def address(self) -> str:
        return self._address
