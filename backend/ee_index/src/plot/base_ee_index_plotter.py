from datetime import timedelta

import matplotlib.pyplot as plt
import numpy as np
from ee_index.src.constant.complement import Smooth
from ee_index.src.constant.time_relation import Day
from ee_index.src.helper.check_file import is_parent_directory_exist
from scipy.signal import savgol_filter


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
        num_days = data_length // Day.ONE.const
        if num_days <= 2:
            x_tick_labels = [
                (start_datetime + timedelta(minutes=int(i))).strftime("%H:%M")
                for i in x_labels
            ]
            self.ax.set_xlabel("UT Time")
        else:
            x_tick_labels = [
                f"{(start_datetime + timedelta(days=int(i // (data_length // num_days)))).strftime('%m/%d')}"
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

    # def smooth(self, y_axis):
    #    return savgol_filter(y_axis, Smooth.EE.length, Smooth.EE.deg)

    # def interpolate(self, x_axis, y_axis):

    #     """Interpolate the nan values in the y_axis
    #     TODO:
    #         x_interpをオーバライドする必要がある
    #         エラーを出させる
    #     """
    #     nan_indices = np.isnan(y_axis)
    #     x_elements = self.get_total_minutes()
    #     x_interp = np.linspace(0, x_elements - 1, x_elements)
    #     y_interp = np.interp(x_interp, x_axis[~nan_indices], y_axis[~nan_indices])
    #     return x_interp, y_interp

    # def plot_er_figure(self, station, absolte_path):
    #     x_axis = self.set_x_axis()
    #     y_axis = self.calculate_er_values(station)
    #     fig, ax = plt.subplots()
    #     ax.plot(x_axis, y_axis)
    #     # x_interp, y_interp = self.interpolate(x_axis, y_axis)
    #     # y_smooth = self.smooth(y_interp)
    #     # fig, ax = plt.subplots()
    #     # ax.plot(x_interp, y_smooth)
    #     self.customize_er_plot(station, ax)
    #     self.save_figure(absolte_path)
    #     plt.close()

    # def plot_edst_figure(self, absolte_path):
    #     x_axis = self.set_x_axis()
    #     y_axis = self.calculate_edst_values()
    #     x_interp, y_interp = self.interpolate(x_axis, y_axis)
    #     y_smooth = self.smooth(y_interp)
    #     fig, ax = plt.subplots()
    #     ax.plot(x_interp, y_smooth)
    #     self.customize_edst_plot(ax)
    #     self.save_figure(absolte_path)
    #     plt.close()

    # def plot_euel_figure(self, station, absolte_path):
    #     x_axis = self.set_x_axis()
    #     y_axis = self.calculate_euel_values(station)
    #     x_interp, y_interp = self.interpolate(x_axis, y_axis)
    #     y_smooth = self.smooth(y_interp)
    #     fig, ax = plt.subplots()
    #     ax.plot(x_interp, y_smooth)
    #     self.customize_euel_plot(station, ax)
    #     self.save_figure(absolte_path)
    #     plt.close()

    # def plot_ee_figure(self, station, absolute_path):
    #     x_axis = self.set_x_axis()
    #     fig, ax = plt.subplots()
    #     ee_valus = self.calculate_ee_values(station)
    #     er, edst, euel = ee_valus[0], ee_valus[1], ee_valus[2]
    #     ax.plot(x_axis, er, label="ER", color="black", lw=0.5)
    #     ax.plot(x_axis, edst, label="EDst", color="green", lw=0.5)
    #     ax.plot(x_axis, euel, label="EUEL", color="red", lw=0.5)
    #     # er_x_interp, er_interp = self.interpolate(x_axis, er)
    #     # edst_x_interp, edst_interp = self.interpolate(x_axis, edst)
    #     # euel_x_interp, euel_interp = self.interpolate(x_axis, euel)
    #     # er_smooth = self.smooth(er_interp)
    #     # edst_smooth = self.smooth(edst_interp)
    #     # euel_smooth = self.smooth(euel_interp)
    #     # ax.plot(er_x_interp, er_smooth, label="ER", color="black")
    #     # ax.plot(edst_x_interp, edst_smooth, label="EDst", color="green")
    #     # ax.plot(euel_x_interp, euel_smooth, label="EUEL", color="red")
    #     ax.legend()
    #     self.customize_ee_plot(station, ax)
    #     self.save_figure(absolute_path)
    #     plt.close()
