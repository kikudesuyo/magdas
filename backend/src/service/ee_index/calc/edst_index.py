from datetime import datetime

import numpy as np
from src.service.ee_index.calc.er_value import NightEr
from src.service.ee_index.constant.magdas_station import EeIndexStation
from src.service.ee_index.constant.time_relation import Min
from src.service.ee_index.helper.time_utils import DateUtils
from src.service.ee_index.helper.warnings_suppression import NanCalculator


class Edst:
    @staticmethod
    def calc_edst(start_dt: datetime, end_dt: datetime) -> np.ndarray:
        days, hours, minutes = DateUtils.time_diff(start_dt, end_dt)
        data_length = (
            days * Min.ONE_DAY.const + hours * Min.ONE_HOUR.const + minutes + 1
        )
        night_er_list = np.empty((0, data_length), dtype=float)
        for station in EeIndexStation:
            night_er = np.array([])
            night_er_instance = NightEr(station, start_dt, end_dt)
            night_er = np.concatenate((night_er, night_er_instance.extract_night_er()))
            night_er_list = np.vstack((night_er_list, night_er))
        edst = NanCalculator.nanmean(night_er_list)
        return edst

    @staticmethod
    def compute_smoothed_edst(start_dt: datetime, end_dt: datetime) -> np.ndarray:
        edst = Edst.calc_edst(start_dt, end_dt)
        weight = np.ones(60) / 60
        moved_edst = np.convolve(edst, weight, mode="same")
        return moved_edst
