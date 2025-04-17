from datetime import date, datetime, timedelta

import numpy as np
from src.service.ee_index.calc.edst_index import Edst
from src.service.ee_index.calc.er_value import Er
from src.service.ee_index.constant.magdas_station import EeIndexStation


class Euel:
    @staticmethod
    def calc_euel(station: EeIndexStation, start_ut: datetime, end_dt: datetime):
        """Calculate EUEL value for a specific period.

        注意:
        開始時刻と終了時刻は共に含めます
        一分値で計算しているため、start_utとend_utは(year, month, day, hour, minute)の粒度で指定してください
        """
        er = Er(station, start_ut, end_dt).calc_er()
        edst = Edst.calc_edst(start_ut, end_dt)
        return er - edst


def get_local_euel(
    station: EeIndexStation, start_lt: datetime, end_lt: datetime
) -> np.ndarray:
    utc_offset = timedelta(hours=station.time_diff)
    start_utc = (start_lt - utc_offset).replace(second=0, microsecond=0)
    end_utc = (end_lt - utc_offset).replace(second=0, microsecond=0)
    return Euel.calc_euel(station, start_utc, end_utc)


def has_night_euel(station: EeIndexStation, local_date: date) -> bool:
    s_lt = datetime(local_date.year, local_date.month, local_date.day, 0, 0)
    e_lt = s_lt.replace(hour=23, minute=59)
    euel = get_local_euel(station, s_lt, e_lt)
    dawn_e = euel[0 : 5 * 60]
    dusk_e = euel[19 * 60 : 24 * 60]
    if np.all(np.isnan(dawn_e)) and np.all(np.isnan(dusk_e)):
        return False
    return True
