from datetime import datetime, timedelta
from typing import List

from src.constants.time_relation import TimeUnit
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParam
from src.service.ee_index.factory_ee import EeFactory
from src.service.sanitize_np import sanitize_np


class EeIndexByDays:
    def __init__(self, start_ut: datetime, days: int, station: EeIndexStation):
        self.start_ut = start_ut
        self.days = days
        self.station = station

    def get_ee_index(self):
        period = Period(self.start_ut, self.start_ut + timedelta(days=self.days))
        params = StationParam(station=self.station, period=period)
        factory = EeFactory()
        er = factory.create_er(params)
        edst = factory.create_edst(period)
        euel = factory.create_euel(params)
        return (
            sanitize_np(er.calc_er()),
            sanitize_np(edst.calc_edst()),
            sanitize_np(euel.calc_euel()),
        )

    def get_minute_labels(self) -> List[str]:
        return [
            (self.start_ut + timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M")
            for i in range(self.days * TimeUnit.ONE_DAY.min)
        ]
