from typing import Union

from fastapi import FastAPI

import requests

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/location/{place_name}/")
def get_coordinate(place_name, prefecture= ""):
    """
    国土地理院APIを使用して、住所から緯度経度を取得する関数。
    """
    url = "https://msearch.gsi.go.jp/address-search/AddressSearch"
    params = {"q": place_name}
    r = requests.get(url, params=params)
    print(f"r: {r}")
    data = r.json()
    if "error" in data:
        print(data["error"])
        return None, None
    if not data:
        return None, None
    else:
        # レスポンスと施設名が一致する緯度経度を返す
        for row in data:
            if row["properties"]["title"].startswith(place_name):
                coordinate = row["geometry"]["coordinates"]
                title = row["properties"]["title"]
                print("🩷")
                return print(coordinate)
        # レスポンス値と都道府県が一致する緯度経度を返す
        for row in data:
            if row["properties"]["title"].startswith(prefecture):
                coordinates = row["geometry"]["coordinates"]
                title = row["properties"]["title"]
                return coordinates, title
        # 見つからない場合
        return None, None


@app.get("/coordinate/{lat}/{lon}/")
def get_location(lat, lon):
    url = f"https://mreversegeocoder.gsi.go.jp/reverse-geocoder/LonLatToAddress?lat={lat}&lon={lon}"
    response = requests.get(url)
    data = response.json()

    if "results" in data:
        address = data["results"]["lv01Nm"]
        return data
    else:
        print("住所情報が見つかりませんでした。")

"""
[
  [
    lon = 132.1442749,
    lat = 34.959377
  ],
  "島根県立しまね海洋館(アクアス)"

"https://mreversegeocoder.gsi.go.jp/reverse-geocoder/LonLatToAddress?lat=34.959377&lon=132.1442749"
"https://mreversegeocoder.gsi.go.jp/reverse-geocoder/LonLatToAddress?lat=43.0686718333333&lon=141.351173694444"
]
"""

def main():
    lat = 34.959377,
    lon = 132.1442749
    location = get_location(lat, lon)
    print(location)

    place_name  = "島根県立しまね海洋館(アクアス)"
    place = get_coordinate(place_name, prefecture= "")
    print(place)



if __name__ == "__main__":
    main()
