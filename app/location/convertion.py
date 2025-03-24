import requests


class GeocodingService:
    def __init__(self):
        pass


def convert_to_coordinates(place_name: str) -> list:
    """
    国土地理院APIを使用して、住所から緯度経度を取得する関数。
    """
    url = "https://msearch.gsi.go.jp/address-search/AddressSearch"
    params = {"q": place_name}
    r = requests.get(url, params=params)
    data = r.json()
    if "error" in data:
        return None, None
    if not data:
        return None, None
    else:
        # レスポンスと施設名が一致する緯度経度を返す
        for row in data:
            if row["properties"]["title"].startswith(place_name):
                coordinate = row["geometry"]["coordinates"]
                title = row["properties"]["title"]
                return coordinate, title
        return None, None


# 秋芳洞 34.22795,131.303069


def convert_to_location(lon: float, lat: float) -> str:
    """
    経度緯度から地点名に変換する関数
        longitude (float): 経度
        latitude (float): 緯度
    """
    pass


def main():
    place = "厳島神社"
    point = convert_to_coordinates(place)
    print(point)


if __name__ == "__main__":
    main()
