from datetime import datetime

import numpy as np

from ee_index.src.constant.magdas_station import EeIndexStation
from ee_index.src.constant.time_relation import DawnAndDusk, Min
from ee_index.src.get_index.er_value import Er, NightEr
from ee_index.src.helper.time_utils import DateUtils
from ee_index.src.helper.warnings_suppression import NanCalculator


class Edst:
    @staticmethod
    def calc_for_min(target_datetime: datetime):
        night_er_list = np.array([])
        for station in EeIndexStation:
            local_datetime = DateUtils.convert_to_local_time(
                station.code, target_datetime
            )
            if (
                local_datetime.time() >= DawnAndDusk.NIGHTSIDE.start
                or local_datetime.time() <= DawnAndDusk.NIGHTSIDE.end
            ):
                er_instance = Er(station.code, DateUtils.get_day_start(target_datetime))
                er = er_instance.calc_er_for_min(target_datetime.time())
                night_er_list = np.append(night_er_list, er)
        edst = NanCalculator.nanmean(night_er_list)
        return edst

    @staticmethod
    def calc_for_days(datetime: datetime, days: int):
        night_er_list = np.empty((0, Min.ONE_DAY.const * days), dtype=float)
        for station in EeIndexStation:
            night_er = np.array([])
            night_er_instance = NightEr(station.code, datetime, days)
            night_er = np.concatenate((night_er, night_er_instance.extract_night_er()))
            night_er_list = np.vstack((night_er_list, night_er))
        edst = NanCalculator.nanmean(night_er_list)
        return edst

    @staticmethod
    def compute_smoothed_edst(datetime: datetime, days: int):
        edst = Edst.calc_for_days(datetime, days)
        weight = np.ones(60) / 60
        moved_edst = np.convolve(edst, weight, mode="same")
        return moved_edst
