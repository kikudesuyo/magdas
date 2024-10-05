from datetime import datetime

import numpy as np
from constant.time_relation import Min
from get_index.edst_index import Edst
from get_index.er_value import Er
from get_index.euel_index import Euel
from helper.time_utils import DateUtils
from plot.base_ee_index_plotter import BaseEeIndexPlotter


class MonthlyEeIndexPlotter(BaseEeIndexPlotter):
    def __init__(self, year: int, month: int, is_ut=False):
        """Constructor
        Args:
          station (str):
          local_datetime (datetime.datetime):
        """
        self.year = year
        self.month = month
        self.days = DateUtils.get_days_in_month(year, month)
        self.total_minutes = self.days * Min.ONE_DAY.const
        self.is_ut = is_ut
        self.start_date = datetime(year, month, 1)
        if is_ut:
            self.start_ut = self.start_date
        else:
            self.start_local_datetime = self.start_date

    def calculate_er_values(self, station):
        return Er(station, self.start_local_datetime).calc_er_for_days(self.days)

    def calculate_edst_values(self):
        return Edst.calc_for_days(self.start_ut, self.days)

    def calculate_euel_values(self, station):
        return Euel.calc_for_month(station, self.year, self.month)

    def calculate_ee_values(self, station):
        if not self.is_ut:
            self.start_ut = DateUtils.convert_to_ut_time(
                station, self.start_local_datetime
            )
        er = self.calculate_er_values(station)
        edst = self.calculate_edst_values()
        euel = self.calculate_euel_values(station)
        return np.array([er, edst, euel])

    def set_x_axis(self):
        return np.arange(0, self.total_minutes, 1)

    def customize_er_plot(self, station, ax):
        ax.set_title(
            f"{self.year}_{self.month}_{station}_LT",
            loc="center",
            fontsize=12,
            fontweight="bold",
        )
        ax.set_xlabel("Days")
        ax.set_ylabel("ER Value(nT)")
        self._set_label(ax)

    def customize_edst_plot(self, ax):
        ax.set_title(
            f"{self.year}_{self.month}", loc="center", fontsize=12, fontweight="bold"
        )
        ax.set_xlabel("Days")
        ax.set_ylabel("EDst Value(nT)")
        self._set_label(ax)

    def customize_euel_plot(self, station, ax):
        ax.set_title(
            f"{self.year}_{self.month}_{station}_LT",
            loc="center",
            fontsize=12,
            fontweight="bold",
        )
        ax.set_xlabel("Days")
        ax.set_ylabel("EUEL Value(nT)")
        self._set_label(ax)

    def customize_ee_plot(self, station, ax):
        ax.set_title(
            f"{self.year}_{self.month}_{station}_LT",
            loc="center",
            fontsize=12,
            fontweight="bold",
        )
        ax.set_xlabel("Days")
        ax.set_ylabel("EE Value(nT)")
        self._set_label(ax)

    def _set_label(self, ax):
        ax.set_xlim(0, self.total_minutes)
        ax.set_xticks(np.arange(0, self.total_minutes, Min.FIVE_DAYS.const))
        ax.set_xticklabels(
            [
                f"{(i//Min.ONE_DAY.const)}"
                for i in np.arange(0, self.total_minutes, Min.FIVE_DAYS.const)
            ]
        )
