from datetime import datetime

import numpy as np
from ee_index.src.calc.edst_index import Edst
from ee_index.src.calc.er_value import Er
from ee_index.src.calc.euel_index import Euel
from ee_index.src.plot.base_ee_index_plotter import BaseEeIndexPlotter


class MultiDayEeIndexPlotter:
    """Plotter for daily EE index"""

    def __init__(self, start_datetime: datetime, end_datetime: datetime):
        self.start_datetime = start_datetime
        self.days = (end_datetime - start_datetime).days + 1
        self.base_plotter = BaseEeIndexPlotter()

    def calc_ee_values(self, station):
        er = Er(station, self.start_datetime).calc_er_for_days(self.days)
        edst = Edst.compute_smoothed_edst(self.start_datetime, self.days)
        euel = Euel.calculate_euel_for_days(station, self.start_datetime, self.days)
        return np.array([er, edst, euel])

    def save_er_figure(self, station, save_path):
        er = Er(station, self.start_datetime).calc_er_for_days(self.days)
        self.base_plotter.plot_er(er)
        self.base_plotter.customize_er_plot(station, self.start_datetime, len(er))
        self.base_plotter.save_figure(save_path)

    def save_edst_figure(self, save_path):
        edst = Edst.compute_smoothed_edst(self.start_datetime, self.days)
        self.base_plotter.plot_edst(edst)
        self.base_plotter.customize_edst_plot(self.start_datetime, len(edst))
        self.base_plotter.save_figure(save_path)

    def save_euel_figure(self, station, save_path):
        euel = Euel.calculate_euel_for_days(station, self.start_datetime, self.days)
        self.base_plotter.plot_euel(euel)
        self.base_plotter.customize_euel_plot(station, self.start_datetime, len(euel))
        self.base_plotter.save_figure(save_path)

    def save_ee_figure(self, station, save_path):
        er = Er(station, self.start_datetime).calc_er_for_days(self.days)
        edst = Edst.compute_smoothed_edst(self.start_datetime, self.days)
        euel = Euel.calculate_euel_for_days(station, self.start_datetime, self.days)
        self.base_plotter.plot_ee(er, edst, euel)
        self.base_plotter.customize_ee_plot(station, self.start_datetime, len(er))
        self.base_plotter.save_figure(save_path)
