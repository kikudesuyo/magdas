from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

from src.constants.time_relation import TimeUnit
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParam
from src.service.calc_utils.sanitize_np import sanitize_np
from src.service.ee_index.factory_ee import EeFactory


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
        factory = EeFactory()
        er = factory.create_er(params)
        edst = factory.create_edst(period)
        euel = factory.create_euel(params)
        return EeData(
            er=sanitize_np(er.calc_er()),
            edst=sanitize_np(edst.calc_edst()),
            euel=sanitize_np(euel.calc_euel()),
            minuteLabels=self._get_minute_labels(),
        )

    def _get_minute_labels(self) -> List[str]:
        return [
            (self.start_ut + timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M")
            for i in range(self.days * TimeUnit.ONE_DAY.min)
        ]
