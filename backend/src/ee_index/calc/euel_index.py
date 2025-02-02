from datetime import datetime

from src.ee_index.calc.edst_index import Edst
from src.ee_index.calc.er_value import Er
from src.ee_index.helper.time_utils import DateUtils


class Euel:
    @staticmethod
    def calc_euel(station, start_dt: datetime, end_dt: datetime):
        """Calculate EUEL value for a specific period.

        注意:
        開始時刻と終了時刻は共に含めます
        一分値で計算しているため、start_dtとend_dtは(year, month, day, hour, minute)の粒度で指定してください
        """
        required_days = (end_dt.date() - start_dt.date()).days + 1
        er = Er(station, start_dt).calc_er_for_days(required_days)
        edst = Edst.compute_smoothed_edst(start_dt, required_days)
        return er - edst

    @staticmethod
    def calc_euel_for_days(station, datetime: datetime, days):
        """開始時刻(00:00ではなく指定時刻)からdays日分のEUEL値を計算します
        TODO: 引数は開始時刻と終了時刻にする
        """
        er = Er(station, datetime).calc_er_for_days(days)
        # edst = Edst.calc_for_days(datetime, days)
        edst = Edst.compute_smoothed_edst(datetime, days)
        euel = er - edst
        return euel

    @staticmethod
    def calc_for_month(station, year, month):
        days = DateUtils.get_days_in_month(year, month)
        start_date = datetime(year, month, 1)
        return Euel.calc_euel_for_days(station, start_date, days)

    @staticmethod
    def calc_for_year(station, year):
        days = DateUtils.get_days_in_year(year)
        start_date = datetime(year, 1, 1)
        return Euel.calc_euel_for_days(station, start_date, days)
