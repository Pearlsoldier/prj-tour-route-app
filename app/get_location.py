import requests

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
                return coordinate, title
        # レスポンス値と都道府県が一致する緯度経度を返す
        for row in data:
            if row["properties"]["title"].startswith(prefecture):
                coordinates = row["geometry"]["coordinates"]
                title = row["properties"]["title"]
                return print(coordinates)
        # 見つからない場合
        return None, None
       
coordinates1,title1 = get_coordinate("厳島神社")
print("有名施設：",coordinates1,title1)

# 秋芳洞 34.22795,131.303069

