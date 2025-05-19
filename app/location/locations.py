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
        self.cordinates = geocoding.get_coordinate(location)
        self._longitude = self.cordinate[1]
        self._latitude = self.cordinate[0]
        reversegeocoding = ReverseGeocoding()
        self._address = reversegeocoding.get_address(self.cordinate[1], self.cordinate[0])

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



