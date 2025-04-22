from datetime import datetime, time, timedelta

import numpy as np
from src.service.ee_index.calc.edst_index import Edst
from src.service.ee_index.calc.er_value import Er
from src.service.ee_index.constant.magdas_station import EeIndexStation


class Euel:
    @staticmethod
    def calc_euel(station: EeIndexStation, start_ut: datetime, end_ut: datetime):
        """Calculate EUEL value for a specific period.

        注意:
        開始時刻と終了時刻は共に含めます
        一分値で計算しているため、start_utとend_utは(year, month, day, hour, minute)の粒度で指定してください
        """
        er = Er(station, start_ut, end_ut).calc_er()
        edst = Edst.calc_edst(start_ut, end_ut)
        return er - edst


class EuelLt:
    def __init__(self, station: EeIndexStation, start_lt: datetime, end_lt: datetime):
        self.station = station
        self.start_lt = start_lt
        self.end_lt = end_lt
        self.euel_values = self.__calc_euel()

    def __calc_euel(self) -> np.ndarray:
        utc_offset = timedelta(hours=self.station.time_diff)
        start_ut = (self.start_lt - utc_offset).replace(second=0, microsecond=0)
        end_ut = (self.end_lt - utc_offset).replace(second=0, microsecond=0)
        return Euel.calc_euel(self.station, start_ut, end_ut)

    def has_night_data(self) -> bool:
        """一日の夜間データが存在するかどうかを判定する"""
        if self.start_lt.date() != self.end_lt.date():
            raise ValueError("start_lt and end_lt must be the same date.")
        if self.start_lt.time() != time(0, 0) or self.end_lt.time() != time(23, 59):
            raise ValueError("start_lt must be 00:00 and end_lt must be 23:59.")
        dawn_e = self.euel_values[0 : 5 * 60]
        dusk_e = self.euel_values[19 * 60 : 24 * 60]
        return not (np.all(np.isnan(dawn_e)) and np.all(np.isnan(dusk_e)))
