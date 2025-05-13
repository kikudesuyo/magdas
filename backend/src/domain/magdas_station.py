from dataclasses import dataclass


@dataclass
class MagdasStation:
    code: str
    time_diff: float
    gm_lat: float
    gm_lon: float
