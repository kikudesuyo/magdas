from datetime import datetime

import numpy as np
from ee_index.src.calc.edst_index import Edst
from ee_index.src.calc.er_value import Er
from ee_index.src.calc.euel_index import Euel


def get_py_ee(station, date: datetime, days: int) -> np.ndarray:
    er = Er(station, date).calc_er_for_days(days)
    edst = Edst.compute_smoothed_edst(date, days)
    euel = Euel.calculate_euel_for_days(station, date, days)
    ee = np.array([er, edst, euel])
    return ee
