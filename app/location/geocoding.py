import requests


class Geocoding:
    def __init__(self):
        pass

    def get_coordinate(self, place_name, prefecture) -> list:
        """
        ジオコーディング
        国土地理院APIを使用して、住所から緯度経度を取得する関数。
        """
        self.url = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="
        self.params = {"q": place_name}
        self.r = requests.get(self.url, params=self.params)
        self.data = self.r.json()
        if "error" in self.data:
            return "error data"
        if not self.data:
            return "not data"
        else:
            # レスポンスと施設名が一致する緯度経度を返す
            for row in self.data:
                if row["properties"]["title"].startswith(place_name):
                    coordinate = row["geometry"]["coordinates"]
                    title = row["properties"]["title"]
                    return coordinate, title
            return None, None


class ReverseGeocoding:
    def __init__(self):
        pass

    def get_location(self, lon: float, lat: float) -> str:
        """
        リバースジオコーディング
        経度緯度から地点名に変換する関数
            longitude (float): 経度
            latitude (float): 緯度
        """
        self.url = f"https://mreversegeocoder.gsi.go.jp/reverse-geocoder/LonLatToAddress?lat={lat}&lon={lon}"
        self.r = requests.get(self.url)
        self.data = self.r.json()


# 秋芳洞 34.22795,131.303069


def main():

if __name__ == "__main__":
    main()
