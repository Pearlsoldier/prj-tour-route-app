import sys
import os
# appディレクトリをsys.pathに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from location.locations import Location

import folium



class Mapping:
    def __init__(self, place_name):
        """
        地図の初期化
        地図のインスタンスを生成
        """
        locator = Location(place_name)
        self.lat = locator.lat
        self.lon = locator.lon
        self.map = folium.Map(location=(self.lat, self.lon))

    def plot_marker(self):
        """
        地図にマーカーをプロットするメソッド
        """
        return folium.Marker(location=[self.lat, self.lon]).add_to(self.map)
        

    def mapping(self):
        """
        地図を生成するメソッド
        """
        return self.map.save("map.html")
    