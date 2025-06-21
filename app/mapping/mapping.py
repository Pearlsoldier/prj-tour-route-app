import sys
import os
# appディレクトリをsys.pathに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import folium



class Mapping:
    def __init__(self, place_name, lat, lon, zoom_start):
        """
        地図の初期化
        地図のインスタンスを生成
        """
        self.lat = lat
        self.lon = lon
        self.locator = place_name
        self.map = folium.Map(location=(lat, lon))

    def plot_marker(self):
        """
        地図にマーカーをプロットするメソッド
        """
        return folium.Marker(location=[self.lat, self.lon]).add_to(self.map)
        

    def mapping(self):
        """
        地図を生成するメソッド
        """
        self.map.save("map.html")
        return "map.html"