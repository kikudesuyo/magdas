from datetime import date, datetime

import numpy as np
from get_pyee import get_py_ee
from get_ut_array import get_ut_array
from matplotlib import pyplot as plt
from read_iaga import get_iaga_ee_for_days
from smoothing import remove_outliers
from src.ee_index.constant.time_relation import Min


class Plotter:
    def __init__(self, station, start_datetime, days):
        self.station = station
        self.start_datetime = start_datetime
        self.days = days
        self.ut_array = get_ut_array(self.start_datetime, self.days).astype(date)
        self.ee = get_iaga_ee_for_days(self.station, self.start_datetime, self.days)
        self.er, self.edst, self.euel = self.ee
        self.py_ee = get_py_ee(self.station, self.start_datetime, self.days)

    def interpolate_ee(self):
        er, edst, euel = self.ee
        interplolated_er = remove_outliers(er)
        interplolated_edst = remove_outliers(edst)
        interplolated_euel = remove_outliers(euel)
        inteplolated_ee = np.array(
            [interplolated_er, interplolated_edst, interplolated_euel]
        )
        return inteplolated_ee

    def set_plot(self, ax):
        hours = [f"{i:02d}:00" for i in range(0, 25, 3)]
        ax.set_ylim(-100, 200)
        ax.set_xlim(0, 1440)
        ax.set_xlabel("Time[UT]")
        ax.set_ylabel("H[nT]", rotation=0, labelpad=10, fontsize=12)
        ax.set_xticks(np.arange(0, 1441, 180))
        ax.set_xticklabels(hours)

    def ee_plot(self, absolute_path):
        fig, ax = plt.subplots()
        ee = self.interpolate_ee()
        py_er, py_edst, py_euel = self.py_ee
        x_axis = np.arange(0, Min.ONE_DAY.const, 1)
        ax.plot(x_axis, self.er, color="black", linewidth=1.0, label="ER")
        ax.plot(x_axis, self.edst, color="green", linewidth=1.0, label="EDst")
        ax.plot(x_axis, self.euel, color="red", linewidth=1.0, label="EUEL")
        # ax.plot(x_axis, py_er, color="black", linewidth=0.7, label="pyER")
        # ax.plot(x_axis, py_edst, color="black", linewidth=1.5, label="pyEDst")
        # ax.plot(x_axis, py_euel, color="red", linewidth=0.7, label="pyEUEL")
        legend = ax.legend(loc="upper left")
        for text in legend.get_texts():
            text.set_fontsize(20)
        self.set_plot(ax)
        self.save_figure(absolute_path)

    def save_figure(self, absolute_path):
        plt.savefig(absolute_path)
        plt.clf()


from datetime import datetime

from src.utils.path import generate_abs_path

plot = Plotter("ANC", datetime(2014, 1, 1), 1)
plot.ee_plot(generate_abs_path("/uozumi_ee-index/img/sample_EE-index.png"))
# plot.ee_plot(generate_abs_path("/uozumi_ee-index/img/ANC_pyEE.png"))
