import numpy as np
from src.constants.time_relation import Min
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParams
from src.usecase.ee_index.calc_er import Er
from src.usecase.ee_index.calc_h_component import HComponent
from src.usecase.ee_index.nan_calculator import NanCalculator


class Edst:
    def __init__(
        self,
        period: Period,
    ):
        self.period = period

    def calc_edst(self) -> np.ndarray:
        days, hours, minutes = self.period.time_diff()
        length = days * Min.ONE_DAY + hours * Min.ONE_HOUR + minutes + 1
        night_er_list = np.empty((0, length), dtype=float)
        for station in EeIndexStation:
            params = StationParams(station, self.period)
            h = HComponent(params)
            er = Er(h)
            night_er_val = er.extract_night_er()
            night_er_list = np.vstack((night_er_list, night_er_val))
        edst = NanCalculator.nanmean(night_er_list)
        return edst
