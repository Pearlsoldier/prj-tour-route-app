import sys
import os

# appディレクトリをsys.pathに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import folium


class MapGenerator:
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

    def generate_map_from_plotter(self, map_plotter, filename="map.html"):
        plotted_map = map_plotter.get_map()
        plotted_map.save(filename)
        return filename