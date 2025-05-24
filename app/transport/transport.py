from enum import Enum

class TransportType(Enum):
    WALKING = "徒歩"
    BICYCLE = "自転車"
    CAR = "車"
    
    def __str__(self):
        return self.value