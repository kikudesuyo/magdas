from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
from ee_index.src.calc.edst_index import Edst
from ee_index.src.calc.er_value import Er
from ee_index.src.calc.euel_index import Euel
from ee_index.src.constant.time_relation import Min
from ee_index.src.plot.config import PlotConfig


class EeIndexPlotter:
    def __init__(self, start_date: datetime, end_date: datetime):
        self.start_datetime = start_date
        self.days = (end_date - start_date).days + 1
        PlotConfig.rcparams()
        self.fig, self.ax = plt.subplots()
        self._set_axis_labels(self.start_datetime, self.days * Min.ONE_DAY.const)

    def plot_er(self, station):
        er = Er(station, self.start_datetime).calc_er_for_days(self.days)
        x_axis, y_axis = np.arange(0, len(er), 1), er
        self.ax.plot(x_axis, y_axis, label="ER", color="black", lw=1.3)

    def plot_edst(self):
        edst = Edst.compute_smoothed_edst(self.start_datetime, self.days)
        x_axis, y_axis = np.arange(0, len(edst), 1), edst
        self.ax.plot(x_axis, y_axis, label="EDst", color="green", lw=1.3)

    def plot_euel(self, station, color):
        euel = Euel.calculate_euel_for_days(station, self.start_datetime, self.days)
        x_axis, y_axis = np.arange(0, len(euel), 1), euel
        self.ax.plot(x_axis, y_axis, label=f"{station}_EUEL", color=color, lw=1.3)

    def plot_ee(self, station):
        er = Er(station, self.start_datetime).calc_er_for_days(self.days)
        edst = Edst.compute_smoothed_edst(self.start_datetime, self.days)
        euel = Euel.calculate_euel_for_days(station, self.start_datetime, self.days)
        if len(er) != len(edst) or len(er) != len(euel):
            raise ValueError("The length of the arrays must be the same")
        x_axis = np.arange(0, len(er), 1)
        self.ax.plot(x_axis, er, label="ER", color="black", lw=0.5)
        self.ax.plot(x_axis, edst, label="EDst", color="green", lw=0.5)
        self.ax.plot(x_axis, euel, label="EUEL", color="red", lw=0.5)

    def _set_axis_labels(self, start_datetime, data_length):
        self.ax.set_ylabel("nT", rotation=0)
        self.ax.set_xlim(0, data_length)
        self.ax.set_ylim(-100, 200)
        self.ax.set_xlabel("Date", fontsize=15)
        tick_interval = max(1, data_length // 8)
        ticks = range(0, data_length, tick_interval)
        time_labels = [
            (start_datetime + timedelta(minutes=i)).strftime("%m/%d %H:%M")
            for i in ticks
        ]
        self.ax.set_xticks(ticks)
        self.ax.set_xticklabels(time_labels)

    def set_title(self, title):
        self.ax.set_title(title, fontsize=15, fontweight="semibold", pad=10)

    def show(self):
        self.ax.legend(loc="lower left", fontsize=18)
        plt.show()

    def save(self, path):
        """画像保存

        Caution:
            show後に呼び出すと白い画面が表示される
        """
        self.ax.legend(loc="lower left", fontsize=18)
        plt.savefig(path)
