from datetime import time, timedelta

import numpy as np
from src.service.ee_index.calc.edst import Edst
from src.service.ee_index.calc.er import Er
from src.service.ee_index.calc.h_component_extraction import HComponent
from src.service.ee_index.helper.params import CalcParams, Period


class Euel:
    def __init__(self, er: Er, edst: Edst):
        self.er = er
        self.edst = edst

    def calc_euel(self) -> np.ndarray:
        return self.er.calc_er() - self.edst.calc_edst()
        # return self.er.calc_er() - self.edst.compute_smoothed_edst()


def create_euel(params: CalcParams) -> Euel:
    h = HComponent(params)
    er = Er(h)
    edst = Edst(params.period)
    return Euel(er, edst)


class EuelLt:
    def __init__(self, p: CalcParams):
        self.p = p
        self.start_lt = p.period.start
        self.end_lt = p.period.end
        ut_param = self.__set_ut_params()
        self.euel = create_euel(ut_param)
        self.euel_values = self.euel.calc_euel()

    def __set_ut_params(self) -> CalcParams:
        utc_offset = timedelta(hours=self.p.station.time_diff)
        start_ut = (self.start_lt - utc_offset).replace(second=0, microsecond=0)
        end_ut = (self.end_lt - utc_offset).replace(second=0, microsecond=0)
        return CalcParams(self.p.station, Period(start_ut, end_ut))

    def has_night_data(self) -> bool:
        """一日の夜間データが存在するかどうかを判定する"""
        if self.start_lt.date() != self.end_lt.date():
            raise ValueError("start_lt and end_lt must be the same date.")
        if self.start_lt.time() != time(0, 0) or self.end_lt.time() != time(23, 59):
            raise ValueError("start_lt must be 00:00 and end_lt must be 23:59.")
        dawn_e = self.euel_values[0 : 5 * 60]
        dusk_e = self.euel_values[19 * 60 : 24 * 60]
        return not (np.all(np.isnan(dawn_e)) and np.all(np.isnan(dusk_e)))
