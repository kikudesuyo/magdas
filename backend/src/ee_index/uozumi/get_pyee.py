from datetime import datetime, timedelta

import numpy as np
from src.ee_index.calc.edst_index import Edst
from src.ee_index.calc.er_value import Er
from src.ee_index.calc.euel_index import Euel


def get_py_ee(station, date: datetime, days: int) -> np.ndarray:
    end_dt = date + timedelta(days=days, minutes=-1)
    er = Er(station, date, end_dt).calc_er()
    edst = Edst.compute_smoothed_edst(date, end_dt)
    euel = Euel.calc_euel(station, date, end_dt)
    ee = np.array([er, edst, euel])
    return ee
