from datetime import timedelta

import numpy as np
from src.service.ee_index.calc.h_component import HComponent
from src.service.ee_index.calc.nan_calculator import NanCalculator
from src.service.ee_index.constant.er_threshold import MAX_ER_VALUE, MIN_ER_VALUE
from src.service.ee_index.constant.time_relation import DawnAndDusk
from src.utils.date import DateUtils


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

    def get_lt_array(self) -> np.ndarray:
        total_minutes = int((self.h.end_ut - self.h.start_ut).total_seconds() // 60) + 1
        lt_arr = []
        for i in range(total_minutes):
            lt = DateUtils.to_lt(
                self.h.station, self.h.start_ut + timedelta(minutes=i)
            ).time()
            lt_arr.append(lt)
        return np.array(lt_arr)

    def nighttime_mask(self) -> np.ndarray:
        lt_arr = self.get_lt_array()
        return np.array([DawnAndDusk.NIGHTSIDE.contains(lt) for lt in lt_arr])

    def extract_night_er(self) -> np.ndarray:
        """Night definition 18:00 to 05:59"""
        night_er = np.where(
            self.nighttime_mask(),
            self.calc_er(),
            np.nan,
        )
        return night_er
