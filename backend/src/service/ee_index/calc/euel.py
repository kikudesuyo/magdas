import numpy as np
from src.service.ee_index.calc.edst import Edst
from src.service.ee_index.calc.er import Er


class Euel:
    def __init__(self, er: Er, edst: Edst):
        self.er = er
        self.edst = edst

    def calc_euel(self) -> np.ndarray:
        return self.er.calc_er() - self.edst.calc_edst()
        # return self.er.calc_er() - self.edst.compute_smoothed_edst()
