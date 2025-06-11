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
class InterfaceAdministrator:
    place: str

    def __str__(self):
        return self.place


@dataclass
class InterfaceBatch:
    batch_locations: list[str] = field(default_factory=list)


@dataclass
class CidInterfaceBatch():
    location: str
    genre_name: str
    location_id: str
    id: str
