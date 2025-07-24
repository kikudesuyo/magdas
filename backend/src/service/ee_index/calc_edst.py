import numpy as np
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParam
from src.service.ee_index.calc_er import Er
from src.service.ee_index.calc_h_component import HComponent
from src.service.nan_calculator import NanCalculator


class Edst:
    def __init__(self, ut_period: Period):
        self.ut_period = ut_period

    def calc_edst(self) -> np.ndarray:
        length = self.ut_period.total_minutes() + 1  # +1 for the start time
        night_er_list = np.empty((0, length), dtype=float)
        for station in EeIndexStation:
            params = StationParam(station, self.ut_period)
            h = HComponent(params)
            er = Er(h.get_equatorial_h())
            night_er_val = er.extract_night_er()
            night_er_list = np.vstack((night_er_list, night_er_val))
        edst = NanCalculator.nanmean(night_er_list)
        return edst
