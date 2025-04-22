from datetime import time, timedelta

import numpy as np
from src.service.ee_index.calc.edst_index import Edst
from src.service.ee_index.calc.er_value import Er
from src.service.ee_index.calc.factory import EeFactory
from src.service.ee_index.calc.h_component_extraction import HComponent
from src.service.ee_index.constant.magdas_station import EeIndexStation
from src.service.ee_index.helper.params import CalcParams, Period


class Euel:
    """Calculate EUEL value for a specific period.
    注意:
    開始時刻と終了時刻は共に含めます
    一分値で計算しているため、start_utとend_utは(year, month, day, hour, minute)の粒度で指定してください
    """

    def __init__(self, params: CalcParams):
        self.p = params

    def calc_euel(self) -> np.ndarray:
        h = HComponent(self.p)
        er = Er(h).calc_er()
        edst = Edst(self.p.period).calc_edst()
        # edst = Edst(self.p.period).compute_smoothed_edst()
        return er - edst


# class EuelCalc:
#     def __init__(self, er: Er, edst: Edst):
#         self.er = er
#         self.edst = edst

#     def calc_euel(self) -> np.ndarray:
#         return self.er.calc_er() - self.edst.compute_smoothed_edst()


class EuelLt:
    def __init__(self, params: CalcParams):
        self.p = params
        self.start_lt, self.end_lt = params.period.start, params.period.end
        self.euel_values = self.__calc_euel()

    def __calc_euel(self) -> np.ndarray:
        utc_offset = timedelta(hours=self.p.station.time_diff)
        start_ut = (self.start_lt - utc_offset).replace(second=0, microsecond=0)
        end_ut = (self.end_lt - utc_offset).replace(second=0, microsecond=0)
        p = CalcParams(self.p.station, Period(start_ut, end_ut))
        return Euel(p).calc_euel()

    def has_night_data(self) -> bool:
        """一日の夜間データが存在するかどうかを判定する"""
        if self.start_lt.date() != self.end_lt.date():
            raise ValueError("start_lt and end_lt must be the same date.")
        if self.start_lt.time() != time(0, 0) or self.end_lt.time() != time(23, 59):
            raise ValueError("start_lt must be 00:00 and end_lt must be 23:59.")
        dawn_e = self.euel_values[0 : 5 * 60]
        dusk_e = self.euel_values[19 * 60 : 24 * 60]
        return not (np.all(np.isnan(dawn_e)) and np.all(np.isnan(dusk_e)))
