from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

from src.constants.time_relation import TimeUnit
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParam
from src.service.calc_utils.sanitize_np import sanitize_np
from src.service.ee_index.magdas_ee import MagdasEeService


@dataclass
class EeData:
    er: List
    edst: List
    euel: List
    minuteLabels: List[str]


class EeIndexByDaysUsecase:
    def __init__(self, start_ut: datetime, days: int, station: EeIndexStation):
        self.start_ut = start_ut
        self.days = days
        self.station = station

    def get_ee_data(self) -> EeData:
        period = Period(self.start_ut, self.start_ut + timedelta(days=self.days))
        params = StationParam(station=self.station, period=period)
        factory = MagdasEeService(params)
        ee_data = factory.calc_all()
        return EeData(
            er=sanitize_np(ee_data.er),
            edst=sanitize_np(ee_data.edst),
            euel=sanitize_np(ee_data.euel),
            minuteLabels=self._minute_labels(),
        )

    def _minute_labels(self) -> List[str]:
        return [
            (self.start_ut + timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M")
            for i in range(self.days * TimeUnit.ONE_DAY.min)
        ]
