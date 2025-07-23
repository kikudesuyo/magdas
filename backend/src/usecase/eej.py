from datetime import date, timedelta
from typing import List

import numpy as np
from src.constants.time_relation import TimeUnit
from src.domain.magdas_station import EeIndexStation
from src.domain.region import Region
from src.domain.station_params import Period, StationParam
from src.service.ee_index.factory_ee import EeFactory
from src.service.eej import PeculiarEejService
from src.service.moving_avg import calc_moving_avg
from src.service.nan_calculator import NanCalculator
from src.service.sanitize_np import sanitize_np


class EejUsecase:
    def __init__(self, start_lt, days, region: Region):
        self.start_lt = start_lt
        self.days = days
        self.region = region

    def get_peculiar_eej_dates(self) -> List[date]:
        service = PeculiarEejService()
        return service.get_dates_by_region(self.region)

    def _calc_avg_euel(self, stations: List[EeIndexStation]) -> np.ndarray:
        f = EeFactory()
        lt_period = Period(self.start_lt, self.start_lt + timedelta(days=self.days))

        euel_values = []
        for station in stations:
            params = StationParam(station=station, period=lt_period).to_ut_params()
            euel = f.create_euel(params)
            euel_values.append(euel.calc_euel())

        if euel_values:
            return NanCalculator.nanmean(np.array(euel_values), axis=0)
        else:
            return np.array([])

    def get_minute_labels(self) -> List[str]:
        return [
            (self.start_lt + timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M")
            for i in range(self.days * TimeUnit.ONE_DAY.min)
        ]

    def get_local_euel(self) -> tuple[List[float | None], List[float | None]]:
        if self.region.code != "south_america":
            raise ValueError(
                "Only 'south_america' region is supported for EEJ detection."
            )
        dip_stations = [
            EeIndexStation.ANC,
            EeIndexStation.HUA,
        ]
        offdip_stations = [EeIndexStation.EUS]

        dip_euel = self._calc_avg_euel(dip_stations)
        offdip_euel = self._calc_avg_euel(offdip_stations)

        dip_euel = calc_moving_avg(dip_euel, 180, 90)
        offdip_euel = calc_moving_avg(offdip_euel, 180, 90)
        return sanitize_np(dip_euel), sanitize_np(offdip_euel)
