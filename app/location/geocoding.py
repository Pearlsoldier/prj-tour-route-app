import requests


class Geocoding:
    def __init__(self, place_name: str):
        self.place = place_name
        url = f"https://msearch.gsi.go.jp/address-search/AddressSearch?q={self.place}"
        params = {"q": place_name}
        r = requests.get(url, params=params)
        self.data = r.json()

    def get_coordinate(self) -> list:
        """
        ジオコーディング
        国土地理院APIを使用して、住所から緯度経度を取得する関数。
        """
        if "error" in self.data:
            return "error data"
        if not self.data:
            return "not data"
        else:
            # レスポンスと施設名が一致する緯度経度を返す
            for row in self.data:
                if row["properties"]["title"].startswith(self.place):
                    coordinates = row["geometry"]["coordinates"]
                    return coordinates
            return None

def main():
    geo = Geocoding("東京駅")
    result = geo.get_coordinate()
    print(result)


if __name__ == "__main__":
    main()