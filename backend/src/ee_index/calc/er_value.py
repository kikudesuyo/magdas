from datetime import datetime, timedelta

import numpy as np
from src.ee_index.calc.h_component_extraction import HComponent
from src.ee_index.constant.er_threshold import MAX_ER_VALUE, MIN_ER_VALUE
from src.ee_index.constant.time_relation import DawnAndDusk
from src.ee_index.helper.time_utils import DateUtils
from src.ee_index.helper.warnings_suppression import NanCalculator


class Er:
    def __init__(self, station, start_dt: datetime, end_dt: datetime):
        self.station = station
        self.start_dt = start_dt
        self.end_dt = end_dt

    def calc_base_value(self) -> np.ndarray:
        """Callculate the daily median of the h component for ER calculation"""
        h_component = HComponent().interpolate_h(
            self.station, self.start_dt, self.end_dt
        )
        median = NanCalculator.nanmedian(h_component)
        base_values = np.repeat(median, len(h_component))
        return base_values

    def calc_er(self):
        h_component = HComponent().interpolate_h(
            self.station, self.start_dt, self.end_dt
        )
        base_values = self.calc_base_value()
        raw_er = h_component - base_values
        er = self.remove_er_outliers(raw_er)
        return er

    def remove_er_outliers(self, rough_er: np.ndarray) -> np.ndarray:
        """Remove outliers from ER value"""
        rough_er[rough_er > MAX_ER_VALUE] = np.nan
        rough_er[rough_er < MIN_ER_VALUE] = np.nan
        return rough_er


class NightEr:
    def __init__(self, station, start_dt: datetime, end_dt: datetime):
        self.station = station
        self.start_dt = start_dt
        self.end_dt = end_dt

    def get_corresponding_local_time(self) -> np.ndarray:
        total_minutes = int((self.end_dt - self.start_dt).total_seconds() // 60) + 1
        local_times = []
        for i in range(total_minutes):
            local_time = DateUtils.to_local_time(
                self.station, self.start_dt + timedelta(minutes=i)
            ).time()
            local_times.append(local_time)
        return np.array(local_times)

    def is_daytime(self) -> np.ndarray:
        condition = np.logical_and(
            DawnAndDusk.DAYSIDE.start <= self.get_corresponding_local_time(),
            self.get_corresponding_local_time() <= DawnAndDusk.DAYSIDE.end,
        )
        return condition

    def extract_night_er(self) -> np.ndarray:
        er = Er(self.station, self.start_dt, self.end_dt).calc_er()
        night_er = np.where(
            self.is_daytime(),
            np.nan,
            er,
        )
        return night_er
