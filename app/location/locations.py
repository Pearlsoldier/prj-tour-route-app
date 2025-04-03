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
        """
        # TODO： 経度・緯度の順番で取れるのか？それとも緯度・経度？
        # FIXME: 緯度経度の順序に合わせてインデックスは修正してください
        # 経度・緯度の順番で取れるが、表記は緯度経度の順序で表記される。
        # 例：北緯XX度、東経YY度
        self._longitude = Coordinate(geocoding[0], "latitude")
        self._latitude= Coordinate(geocoding[1], "longitude")
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
