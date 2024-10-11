from datetime import datetime

from ee_index.src.calc.edst_index import Edst
from ee_index.src.calc.er_value import Er
from ee_index.src.calc.euel_index import Euel
from ee_index.src.constant.time_relation import Day
from ee_index.src.plot.base_ee_index_plotter import BaseEeIndexPlotter


class DailyEeIndexPlotter:
    """Plotter for daily EE index"""

    def __init__(
        self,
        start_datetime: datetime,
    ):
        self.start_datetime = start_datetime
        self.base_plotter = BaseEeIndexPlotter()

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

    def save_er_figure(self, station, save_path):
        er = self.calculate_er_values(station)
        self.base_plotter.plot_er(er)
        self.base_plotter.customize_er_plot(station, self.start_datetime, len(er))
        self.base_plotter.save_figure(save_path)

    def save_edst_figure(self, save_path):
        edst = self.calculate_edst_values()
        self.base_plotter.plot_edst(edst)
        self.base_plotter.customize_edst_plot(self.start_datetime, len(edst))
        self.base_plotter.save_figure(save_path)

    def save_ee_figure(self, station, save_path):
        er, edst, euel = (
            self.calculate_er_values(station),
            self.calculate_edst_values(),
            self.calculate_euel_values(station),
        )
        self.base_plotter.plot_ee(er, edst, euel)
        self.base_plotter.customize_ee_plot(station, self.start_datetime, len(er))
        self.base_plotter.save_figure(save_path)
