import numpy as np
from src.service.ee_index.calc.er_value import NightEr
from src.service.ee_index.constant.magdas_station import EeIndexStation
from src.service.ee_index.constant.time_relation import Min
from src.service.ee_index.helper.nan_calculator import NanCalculator
from src.service.ee_index.helper.params import CalcParams, Period
from src.service.ee_index.helper.time_utils import DateUtils


class Edst:
    def __init__(
        self,
        period: Period,
    ):
        self.period = period

    def calc_edst(self) -> np.ndarray:
        days, hours, minutes = DateUtils.time_diff(self.period)
        data_length = (
            days * Min.ONE_DAY.const + hours * Min.ONE_HOUR.const + minutes + 1
        )
        night_er_list = np.empty((0, data_length), dtype=float)
        for station in EeIndexStation:
            params = CalcParams(station, self.period)
            night_er = NightEr(params)
            night_er_val = night_er.extract_night_er()
            night_er_list = np.vstack((night_er_list, night_er_val))
        edst = NanCalculator.nanmean(night_er_list)
        return edst

    def compute_smoothed_edst(self) -> np.ndarray:
        edst = self.calc_edst()
        weight = np.ones(60) / 60
        moved_edst = np.convolve(edst, weight, mode="same")
        return moved_edst
