import requests


class GeocodingService:
    def __init__(self, url, place_name):
        self.url = "https://msearch.gsi.go.jp/address-search/AddressSearch"
        self.params = {"q": place_name}
        self.r = requests.get(url, params=params)
        self.data = r.json()

    def get_coordinates(place_name: str) -> list:
        """
        国土地理院APIを使用して、住所から緯度経度を取得する関数。
        """
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

    def get_location(lon: float, lat: float) -> str:
        """
        経度緯度から地点名に変換する関数
            longitude (float): 経度
            latitude (float): 緯度
        """
        pass



class CurrentLocation:
    def __init__(self, current_location):
        self.current_location = current_location

class NextLocation:
    def __init__(self, next_location):
        self.next_location = next_location




# 秋芳洞 34.22795,131.303069


def get_location(lon: float, lat: float) -> str:
    """
    経度緯度から地点名に変換する関数
        longitude (float): 経度
        latitude (float): 緯度
    """
    pass


def main():
    place_name = "厳島神社"
    location_instance = CurrentLocation(place_name)
    print(location_instance.current_location)

    place_name = "秋芳洞"
    location_instance = NextLocation(place_name)
    print(location_instance.next_location)


if __name__ == "__main__":
    main()
