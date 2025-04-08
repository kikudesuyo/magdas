from datetime import datetime, timedelta

from src.service.ee_index.calc.edst_index import Edst
from src.service.ee_index.calc.er_value import Er
from src.service.ee_index.constant.magdas_station import EeIndexStation


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


def get_local_euel(
    station: EeIndexStation, local_start_dt: datetime, local_end_dt: datetime
):
    utc_offset = timedelta(hours=station.time_diff)
    start_utc = (local_start_dt - utc_offset).replace(second=0, microsecond=0)
    end_utc = (local_end_dt - utc_offset).replace(second=0, microsecond=0)
    return Euel.calc_euel(station.code, start_utc, end_utc)
