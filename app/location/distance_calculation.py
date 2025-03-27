from locations import Location
import requests

"""
秋芳洞
    lat = 34.22795,
    lon = 131.303069

島根県立しまね海洋館(アクアス)
    lat = 34.959377,
    lon = 132.1442749
"""


class DistanceCalculator:
    def __init__(self, location1, location2):
        OUTPUT_TYPE = "json"
        ELLIPSOID = "GRS80"
        lat1 = location1.lat
        lon1 = location1.lon
        lat2 = location2.lat
        lon2 = location2.lon
        self.cal_api = f"https://vldb.gsi.go.jp/sokuchi/surveycalc/surveycalc/bl2st_calc.pl?outputType={OUTPUT_TYPE}&ellipsoid={ELLIPSOID}&latitude1={lat1}&longitude1={lon1}&latitude2={lat2}&longitude2={lon2}"


    def calculate(self) -> float:
        self.response = requests.get(self.cal_api)
        self.data = self.response.json()
        self.output = self.data["OutputData"]
        return self.output.get("geoLength")