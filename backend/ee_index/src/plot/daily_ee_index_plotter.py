from datetime import datetime

import numpy as np
from ee_index.src.calc.edst_index import Edst
from ee_index.src.calc.er_value import Er
from ee_index.src.calc.euel_index import Euel
from ee_index.src.constant.time_relation import Day, Min
from ee_index.src.plot.base_ee_index_plotter import BaseEeIndexPlotter


class DailyEeIndexPlotter(BaseEeIndexPlotter):
    """Plotter for daily EE index"""

    def __init__(self, start_datetime: datetime):
        self.start_datetime = start_datetime

    def calculate_er_values(self, station):
        return Er(station, self.start_datetime).calc_er_for_days(Day.ONE.const)

    def calculate_edst_values(self):
        return Edst.compute_smoothed_edst(self.start_datetime, Day.ONE.const)

    def calculate_euel_values(self, station):
        return Euel.calculate_euel_for_days(
            station,
            self.start_datetime,
            Day.ONE.const,
        )

    def calculate_ee_values(self, station):
        er = self.calculate_er_values(station)
        edst = self.calculate_edst_values()
        euel = self.calculate_euel_values(station)
        return np.array([er, edst, euel])

    def set_x_axis(self):
        return np.arange(0, Min.ONE_DAY.const, 1)

    def customize_er_plot(self, station, ax):
        ax.set_title(
            f"{self.start_datetime.date()}_{station}_UT",
            loc="center",
            fontsize=12,
            fontweight="bold",
        )
        ax.set_xlabel("UT Time")
        ax.set_ylabel("ER Value(nT)")
        self._set_label(ax)

    def customize_edst_plot(self, ax):
        ax.set_title(
            f"{self.start_datetime.date()}",
            loc="center",
            fontsize=12,
            fontweight="bold",
        )
        ax.set_xlabel("UT Time")
        ax.set_ylabel("EDst Value(nT)")
        self._set_label(ax)

    def customize_euel_plot(self, station, ax):
        ax.set_title(
            f"{self.start_datetime.date()}_{station}_UT",
            loc="center",
            fontsize=12,
            fontweight="bold",
        )
        ax.set_xlabel("UT Time")
        ax.set_ylabel("EUEL Value(nT)")
        self._set_label(ax)

    def customize_ee_plot(self, station, ax):
        ax.set_title(
            f"{self.start_datetime.date()}_{station}_UT",
            loc="center",
            fontsize=12,
            fontweight="bold",
        )
        ax.set_xlabel("UT Time")
        ax.set_ylabel("EEindex Value(nT)")
        ax.set_ylim(-100, 200)
        self._set_label(ax)

    def get_total_minutes(self):
        return Min.ONE_DAY.const

    def _set_label(self, ax):
        ax.set_xlim(0, Min.ONE_DAY.const)
        ax.set_xticks(np.arange(0, Min.ONE_DAY.const, Min.THREE_HOURS.const))
        ax.set_xticklabels(
            [
                f"{i // 60:02d}:{i % 60:02d}"
                for i in np.arange(0, Min.ONE_DAY.const, Min.THREE_HOURS.const)
            ]
        )
