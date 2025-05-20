import numpy as np
from src.usecase.ee_index.calc_edst import Edst
from src.usecase.ee_index.calc_er import Er


class Euel:
    def __init__(self, er: Er, edst: Edst):
        self.er = er
        self.edst = edst

    def calc_euel(self) -> np.ndarray:
        return self.er.calc_er() - self.edst.calc_edst()
