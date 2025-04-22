from dataclasses import dataclass
from datetime import datetime

from src.service.ee_index.constant.magdas_station import EeIndexStation


@dataclass
class Period:
    start: datetime
    end: datetime

    def __post_init__(self):
        if self.start >= self.end:
            raise ValueError("Start time must be before end time.")


@dataclass
class CalcParams:
    station: EeIndexStation
    period: Period
