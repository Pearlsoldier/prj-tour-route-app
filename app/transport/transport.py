from dataclasses import dataclass

@dataclass
class Transport:
    transport_type: str # 移動手段について

    def __str__(self):
        return str(self.transport_type)