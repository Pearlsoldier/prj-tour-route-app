import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import folium

from mapping.mapgenerator import MapGenerator


class MapPlotter:
    def __init__(self, map_instance: folium.map):
        self._map = map_instance

    def plot_point(self, location_instance):
        """
        地図にマーカーをプロットするメソッド
        """
        folium.Marker(
            location=[location_instance.latitude, location_instance.longitude],
            popup=f"出発地点: {location_instance.location}",
        ).add_to(self._map)
        return self

    def plot_circle_mark(self, location_instance, with_in_range):
        folium.Circle(
            location=[location_instance.latitude, location_instance.longitude],
            radius=with_in_range,
            color="#ff0000",
            fill_color="#0000ff",
        ).add_to(self._map)
        return self

    def get_map(self):
        return self._map
