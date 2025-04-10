from datetime import datetime, timedelta

import numpy as np
from src.service.ee_index.calc.h_component_extraction import HComponent
from src.service.ee_index.constant.er_threshold import MAX_ER_VALUE, MIN_ER_VALUE
from src.service.ee_index.constant.magdas_station import EeIndexStation
from src.service.ee_index.constant.time_relation import DawnAndDusk
from src.service.ee_index.helper.nan_calculator import NanCalculator
from src.service.ee_index.helper.time_utils import DateUtils


class Er:
    def __init__(self, station: EeIndexStation, start_ut: datetime, end_ut: datetime):
        self.station = station
        self.start_ut = start_ut
        self.end_ut = end_ut

    def calc_base_value(self) -> np.float32:
        """Callculate the daily median of the h component for ER calculation"""
        h_component = HComponent().to_equatorial_h(
            self.station, self.start_ut, self.end_ut
        )
        return NanCalculator.nanmedian(h_component)

    def calc_er(self):
        h_component = HComponent().to_equatorial_h(
            self.station, self.start_ut, self.end_ut
        )
        raw_er = h_component - self.calc_base_value()
        er = self.remove_er_outliers(raw_er)
        return er

    def remove_er_outliers(self, rough_er: np.ndarray) -> np.ndarray:
        """Remove outliers from ER value"""
        rough_er[rough_er > MAX_ER_VALUE] = np.nan
        rough_er[rough_er < MIN_ER_VALUE] = np.nan
        return rough_er


class NightEr:
    """Night definition 18:00 to 05:59"""

    def __init__(self, station: EeIndexStation, start_ut: datetime, end_ut: datetime):
        self.station = station
        self.start_ut = start_ut
        self.end_ut = end_ut

    def get_corresponding_lt(self) -> np.ndarray:
        total_minutes = int((self.end_ut - self.start_ut).total_seconds() // 60) + 1
        lt_arr = []
        for i in range(total_minutes):
            lt = DateUtils.to_lt(
                self.station, self.start_ut + timedelta(minutes=i)
            ).time()
            lt_arr.append(lt)
        return np.array(lt_arr)

    def is_daytime(self) -> np.ndarray:
        condition = np.logical_and(
            DawnAndDusk.DAYSIDE.start <= self.get_corresponding_lt(),
            self.get_corresponding_lt() <= DawnAndDusk.DAYSIDE.end,
        )
        return condition

    def extract_night_er(self) -> np.ndarray:
        er = Er(self.station, self.start_ut, self.end_ut).calc_er()
        night_er = np.where(
            self.is_daytime(),
            np.nan,
            er,
        )
        return night_er
