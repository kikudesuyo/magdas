from datetime import timedelta

import numpy as np
from src.service.ee_index.calc.h_component_extraction import HComponent
from src.service.ee_index.calc.params import CalcParams
from src.service.ee_index.constant.er_threshold import MAX_ER_VALUE, MIN_ER_VALUE
from src.service.ee_index.constant.time_relation import DawnAndDusk
from src.service.ee_index.helper.nan_calculator import NanCalculator
from src.service.ee_index.helper.time_utils import DateUtils


class Er:
    def __init__(self, h: HComponent):
        self.h = h

    def calc_er(self):
        h_component = self.h.to_equatorial_h()
        base = NanCalculator.nanmedian(h_component)
        raw_er = h_component - base
        return self._remove_outliers(raw_er)

    def _remove_outliers(self, raw_er: np.ndarray) -> np.ndarray:
        raw_er[raw_er > MAX_ER_VALUE] = np.nan
        raw_er[raw_er < MIN_ER_VALUE] = np.nan
        return raw_er


class NightEr:
    """Night definition  18:00 to 05:59"""

    def __init__(self, params: CalcParams):
        self.p = params
        self.station = params.station
        self.start_ut = params.period.start
        self.end_ut = params.period.end

    def get_corresponding_lt(self) -> np.ndarray:
        total_minutes = int((self.end_ut - self.start_ut).total_seconds() // 60) + 1
        lt_arr = []
        for i in range(total_minutes):
            lt = DateUtils.to_lt(
                self.station, self.start_ut + timedelta(minutes=i)
            ).time()
            lt_arr.append(lt)
        return np.array(lt_arr)

    def nighttime_mask(self) -> np.ndarray:
        lt_arr = self.get_corresponding_lt()
        return np.array([DawnAndDusk.NIGHTSIDE.contains(lt) for lt in lt_arr])

    def extract_night_er(self) -> np.ndarray:
        h = HComponent(self.p)
        er = Er(h).calc_er()
        night_er = np.where(
            self.nighttime_mask(),
            er,
            np.nan,
        )
        return night_er
