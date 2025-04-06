from dataclasses import dataclass

@dataclass
class TimeRequired:
    value: int # "分表記で受け付ける"

    def __str__(self):
        return str(self.value) 