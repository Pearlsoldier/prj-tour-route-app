import requests


class Geocoding:
    def __init__(self):
        self.api_url = (
            "https://msearch.gsi.go.jp/address-search/AddressSearch?q={place}"
        )

    def get_coordinate(self, place: str) -> list[float]:
        """
        ジオコーディング
        国土地理院APIを使用して、住所から緯度経度を取得する関数。
        """
        response = requests.get(
            self.api_url.format(place=place), params={"q": place}
        ).json()

        if "error" in response:
            return "error data"
        if not response:
            return "not data"
        else:
            # レスポンスと施設名が一致する緯度経度を返す
            for row in response:
                if row["properties"]["title"].startswith(place):
                    coordinates = row["geometry"]["coordinates"]
                    return coordinates
            return None


class ReverseGeocoding:
    def __init__(self):
        self.api_url = "https://mreversegeocoder.gsi.go.jp/reverse-geocoder/LonLatToAddress?lat={lat}&lon={lon}"

    def get_address(self, lon, lat):
        """
        リバースジオコーディング
        国土地理院APIを使用して緯度経度から住所を取得する関数。
        """
        address_response = requests.get(self.api_url.format(lon=lon, lat=lat))
        data = address_response.json()

        if "results" in data:
            address = data["results"]["lv01Nm"]
            return address
        else:
            print("住所情報が見つかりませんでした。")


class Distance:
    def __init__(self, start_location: str, end_location: str):
        from location.locations import Location

        OUTPUT_TYPE = "json"
        ELLIPSOID = "GRS80"
        start_handler = Location(start_location)
        end_handler = Location(end_location)
        lat1 = start_handler.latitude
        lon1 = start_handler.longitude
        lat2 = end_handler.latitude
        lon2 = end_handler.longitude
        cal_api = f"https://vldb.gsi.go.jp/sokuchi/surveycalc/surveycalc/bl2st_calc.pl?outputType={OUTPUT_TYPE}&ellipsoid={ELLIPSOID}&latitude1={lat1}&longitude1={lon1}&latitude2={lat2}&longitude2={lon2}"
        response = requests.get(cal_api)
        data = response.json()
        print(f"start: {start_location}")
        print(f"end: {end_location}")
        output = data["OutputData"]
        print(output)
        distance_str = output.get("geoLength")
        self._distance = float(distance_str)

    @property
    def distance(self) -> float:
        return self._distance
