import folium

class Map:
    def __init__(self, location):
        """
        地図の初期化
        地図のインスタンスを生成
        """
        lat = location.lat
        lon = location.lon
        self.map = folium.Map(location=(lat, lon))
        return self.map

    def plot_marker(self, location):
        """
        地図にマーカーをプロットするメソッド
        """
        lat = location.lat
        lon = location.lon
        return folium.Marker(location=[lat, lon]).add_to(self.map)
        

    def mapping(self):
        """
        地図を生成するメソッド
        """
        return self.map.save("map.html")
    