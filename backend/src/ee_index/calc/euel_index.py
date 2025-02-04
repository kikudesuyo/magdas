from datetime import datetime

from src.ee_index.calc.edst_index import Edst
from src.ee_index.calc.er_value import Er


class Euel:
    @staticmethod
    def calc_euel(station, start_dt: datetime, end_dt: datetime):
        """Calculate EUEL value for a specific period.

        注意:
        開始時刻と終了時刻は共に含めます
        一分値で計算しているため、start_dtとend_dtは(year, month, day, hour, minute)の粒度で指定してください
        """
        er = Er(station, start_dt, end_dt).calc_er()
        edst = Edst.calc_edst(start_dt, end_dt)
        return er - edst
