from abc import ABC, abstractmethod


class TransportType(ABC):
    @property
    @abstractmethod
    def movement_speed(self):
        """毎分の移動距離を返す。
        徒歩： 80m/min
        自転車: 240m/min
        車(都市部): 280m/min
        """
        pass


class Walk(TransportType):
    @property
    def movement_speed(self) -> int:
        return 70


class Bicycle(TransportType):
    @property
    def movement_speed(self) -> int:
        return 240


class Car(TransportType):
    @property
    def movement_speed(self) -> int:
        return int(280)
