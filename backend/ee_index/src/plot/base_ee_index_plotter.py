from datetime import timedelta

import matplotlib.pyplot as plt
import numpy as np
from ee_index.src.constant.time_relation import Min
from ee_index.src.helper.check_file import is_parent_directory_exist


class BaseEeIndexPlotter:

    def __init__(self):
        self.fig, self.ax = plt.subplots()

    # interpをしたほうがいいいかも
    def plot_er(self, er_values):
        x_axis = np.arange(0, len(er_values), 1)
        y_axis = er_values
        self.ax.plot(x_axis, y_axis)

    def plot_edst(self, edst_values):
        x_axis = np.arange(0, len(edst_values), 1)
        y_axis = edst_values
        self.ax.plot(x_axis, y_axis)

    def plot_euel(self, euel_values):
        x_axis = np.arange(0, len(euel_values), 1)
        y_axis = euel_values
        self.ax.plot(x_axis, y_axis)

    def plot_ee(self, er, edst, euel):
        if len(er) != len(edst) or len(er) != len(euel):
            raise ValueError("The length of the arrays must be the same")
        x_axis = np.arange(0, len(er), 1)
        self.ax.plot(x_axis, er, label="ER", color="black", lw=0.5)
        self.ax.plot(x_axis, edst, label="EDst", color="green", lw=0.5)
        self.ax.plot(x_axis, euel, label="EUEL", color="red", lw=0.5)

    def customize_er_plot(self, station, start_datetime, data_length):
        self._set_title(f"{start_datetime.date()}_{station}_UT")
        self._set_axis_labels("ER Value(nT)", start_datetime, data_length)

    def customize_edst_plot(self, start_datetime, data_length):
        self._set_title(f"{start_datetime.date()}_UT")
        self._set_axis_labels("EDst Value(nT)", start_datetime, data_length)

    def customize_euel_plot(self, station, start_datetime, data_length):
        self._set_title(f"{start_datetime.date()}_{station}_UT")
        self._set_axis_labels("EUEL Value(nT)", start_datetime, data_length)

    def customize_ee_plot(self, station, start_datetime, data_length):
        self._set_title(f"{start_datetime.date()}_{station}_UT")
        self._set_axis_labels("EEindex Value(nT)", start_datetime, data_length)

    def _set_title(self, title):
        self.ax.set_title(title, loc="center", fontsize=12, fontweight="bold")

    def _set_axis_labels(self, y_label_name, start_datetime, data_length):
        self.ax.set_ylabel(y_label_name)
        self.ax.set_xlim(0, data_length)
        self.ax.set_ylim(-100, 200)
        x_labels = np.arange(0, data_length, data_length // 8)
        num_days = data_length // Min.ONE_DAY.const
        # 表示形式の変更
        if num_days <= 2:
            # 時間表示
            x_tick_labels = [
                (start_datetime + timedelta(minutes=int(i))).strftime("%H:%M")
                for i in x_labels
            ]
            self.ax.set_xlabel("UT Time")
        else:
            # 日付表示
            x_tick_labels = [
                (start_datetime + timedelta(days=int(i // Min.ONE_DAY.const))).strftime(
                    "%m/%d"
                )
                for i in x_labels
            ]
            self.ax.set_xlabel("UT Date")
        self.ax.set_xticks(x_labels)
        self.ax.set_xticklabels(x_tick_labels)

    def show_figure(self):
        plt.show()

    def save_figure(self, absolte_path):
        if not is_parent_directory_exist(absolte_path):
            raise FileNotFoundError("Directory does not exist")
        plt.savefig(absolte_path)
        plt.clf()
