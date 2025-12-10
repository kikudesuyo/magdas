import numpy as np
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParam
from src.service.calc_utils.nan_calculator import NanCalculator
from src.service.ee_index.calc.calc_er import MagdasErCalculator
from src.service.ee_index.calc.calc_h_component import MagdasHComponent


class MagdasEdstCalculator:
    def __init__(self, ut_period: Period):
        self.ut_period = ut_period

    def calc(self) -> np.ndarray:
        length = self.ut_period.total_minutes() + 1  # +1 for the start time
        night_er_list = np.empty((0, length), dtype=float)
        for station in EeIndexStation:
            params = StationParam(station, self.ut_period)
            h = MagdasHComponent(params)
            er = MagdasErCalculator(h.calc_equatorial_h())
            night_er_val = er.extract_night_er()
            night_er_list = np.vstack((night_er_list, night_er_val))
        edst = NanCalculator.nanmean(night_er_list)
        return edst

    def get_min_edst(self) -> float:
        return np.nanmin(self.calc())
