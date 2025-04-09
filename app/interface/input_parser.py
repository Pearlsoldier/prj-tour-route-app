from dataclasses import dataclass
"""
入力(施設名、移動手段、所要時間)を受け取りたいので、保存するものとして3点を定義する
挙動として、
ユーザーが入力
何か変数、辞書、リストに保存
それぞれのクラスに、対応するデータが参照できる様にする

"""

@dataclass
class Interface:
    place: str
    transport: str
    transit_time: str

    def __str__(self):
        return (self.place, self.transport, self.transit_time)