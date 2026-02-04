from datetime import date, timedelta
from typing import List, Optional

import numpy as np
from pydantic import BaseModel
from src.constants.time_relation import TimeUnit
from src.domain.magdas_station import EeIndexStation
from src.domain.region import Region
from src.domain.station_params import Period, StationParam
from src.service.calc_utils.moving_avg import calc_moving_avg
from src.service.calc_utils.nan_calculator import NanCalculator
from src.service.calc_utils.sanitize_np import sanitize_np
from src.service.ee_index.magdas_ee import MagdasEuelService
from src.service.peculiar_eej import PeculiarEejService


class EejRow(BaseModel):
    time: str
    dipEuel: Optional[float]
    offdipEuel: Optional[float]


class EejResult(BaseModel):
    data: List[EejRow]
    peculiarEejDates: List[str]


class EejUsecase:
    def __init__(
        self, start_lt, days, region: Region, stations: List[EeIndexStation]
    ):
        self.start_lt = start_lt
        self.days = days
        if not isinstance(region, Region):
            raise ValueError("region must be an instance of Region Enum")
        self.region = region
        self.stations = stations

    def execute(self) -> EejResult:
        peculiar_eej_dates = self._get_peculiar_eej_dates()
        minute_labels = self._minute_labels()
        dip_euel, offdip_euel = self._get_local_euel()

        eej_rows = [
            EejRow(
                time=minute_labels[i],
                dipEuel=dip_euel[i],
                offdipEuel=offdip_euel[i],
            )
            for i in range(len(minute_labels))
        ]
        peculiar_eej_dates_str = [
            date.strftime("%Y-%m-%d") for date in peculiar_eej_dates
        ]

        return EejResult(data=eej_rows, peculiarEejDates=peculiar_eej_dates_str)

    def _get_peculiar_eej_dates(self) -> List[date]:
        service = PeculiarEejService()
        peculiar_eej_data = service.get_by_region(self.region)
        return [data.date for data in peculiar_eej_data]

    def _calc_avg_euel(self, stations: List[EeIndexStation]) -> np.ndarray:
        lt_period = Period(self.start_lt, self.start_lt + timedelta(days=self.days))

        euel_values = []
        for station in stations:
            params = StationParam(station=station, period=lt_period).to_ut_params()
            ee_service = MagdasEuelService(params)
            euel = ee_service.calc()
            euel_values.append(euel)

        if euel_values:
            return NanCalculator.nanmean(np.array(euel_values), axis=0)
        else:
            return np.array([])

    def _minute_labels(self) -> List[str]:
        return [
            (self.start_lt + timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M")
            for i in range(self.days * TimeUnit.ONE_DAY.min)
        ]

    def _get_local_euel(self) -> tuple[List[float | None], List[float | None]]:
        dip_stations = [s for s in self.stations if s.is_dip()]
        offdip_stations = [s for s in self.stations if s.is_offdip()]

        if not dip_stations or not offdip_stations:
            # Fallback to defaults if no suitable stations found, or raise error?
            # For now, let's assume valid stations are passed or rely on error if empty lists cause issues (though _calc_avg_euel returns empty array)
             pass
        dip_euel = self._calc_avg_euel(dip_stations)
        offdip_euel = self._calc_avg_euel(offdip_stations)
        dip_euel = calc_moving_avg(dip_euel, 180, 90)
        offdip_euel = calc_moving_avg(offdip_euel, 180, 90)
        return sanitize_np(dip_euel), sanitize_np(offdip_euel)
