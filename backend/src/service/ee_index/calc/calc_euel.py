from dataclasses import dataclass

import numpy as np


@dataclass
class ErEdst:
    er: np.ndarray
    edst: np.ndarray


class EuelCalculator:
    def __init__(self, er_edst: ErEdst):
        self.er = er_edst.er
        self.edst = er_edst.edst

    def calc(self) -> np.ndarray:
        return self.er - self.edst
