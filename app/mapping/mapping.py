import sys
import os

# appディレクトリをsys.pathに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import folium


class Mapping:
    def __init__(self, place_name: str, lat: int, lon: int, zoom_start: int):
        """
        地図の初期化
        地図のインスタンスを生成
        """
        self.lat = lat
        self.lon = lon
        self.zoom = zoom_start
        self.location = [self.lat, self.lon]
        self.locator = place_name
        self.map = folium.Map(location=self.location, zoom_start=self.zoom)

    def plot_start_mark(self):
        """
        地図にマーカーをプロットするメソッド
        """
        folium.Marker(
            location=[self.lat, self.lon],
            popup=f"出発地点: {self.locator}",
        ).add_to(self.map)
        return self

    def plot_circle_mark(self, with_in_range=None):
        folium.Circle(
            location=self.location,
            radius=with_in_range,
            color="#ff0000",
            fill_color="#0000ff",
        ).add_to(self.map)
        return self

    def mapping(self):
        """
        地図を生成するメソッド
        """
        self.map.save("map.html")
        return "map.html"
