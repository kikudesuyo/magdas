from datetime import datetime

from src.ee_index.calc.edst_index import Edst
from src.ee_index.calc.er_value import Er
from src.ee_index.helper.time_utils import DateUtils


class Euel:
    @staticmethod
    def calculate_euel_for_days(station, datetime: datetime, days):
        er = Er(station, datetime).calc_er_for_days(days)
        # edst = Edst.calc_for_days(datetime, days)
        edst = Edst.compute_smoothed_edst(datetime, days)
        euel = er - edst
        return euel

    @staticmethod
    def calc_for_month(station, year, month):
        days = DateUtils.get_days_in_month(year, month)
        start_date = datetime(year, month, 1)
        return Euel.calculate_euel_for_days(station, start_date, days)

    @staticmethod
    def calc_for_year(station, year):
        days = DateUtils.get_days_in_year(year)
        start_date = datetime(year, 1, 1)
        return Euel.calculate_euel_for_days(station, start_date, days)
