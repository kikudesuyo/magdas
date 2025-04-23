import numpy as np
from src.service.ee_index.calc.edst import Edst
from src.service.ee_index.calc.er import Er
from src.service.ee_index.calc.h_component import HComponent
from src.service.ee_index.helper.params import CalcParams


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


def has_night_data(local_daily_data: np.ndarray) -> bool:
    """一日の夜間データが存在するかどうかを判定する"""
    if len(local_daily_data) != 1440:
        raise ValueError("daily_data must have 1440 elements.")
    dawn_e = local_daily_data[0 : 5 * 60]
    dusk_e = local_daily_data[19 * 60 : 24 * 60]
    return not (np.all(np.isnan(dawn_e)) and np.all(np.isnan(dusk_e)))
