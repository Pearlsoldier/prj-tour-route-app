from dataclasses import dataclass, field

"""
入力(施設名、移動手段、所要時間)を受け取りたいので、保存するものとして3点を定義する
挙動として、
ユーザーが入力
何か変数、辞書、リストに保存
それぞれのクラスに、対応するデータが参照できる様にする

class mode_administrator(管理者)で施設名を受け取る

"""


@dataclass
class Interface:
    place: str
    transport: str
    transit_time: str

    # def __str__(self):
    #     return {"place": self.place, "transport": self.transport, "transit_time": self.transit_time}


@dataclass
class Interface_administrator:
    place: str

    def __str__(self):
        return self.place
    
@dataclass
class Interface_batch:
    places: list[str] = field(default_factory=list)


