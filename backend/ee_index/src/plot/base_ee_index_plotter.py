import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

from ee_index.src.constant.complement import Smooth
from ee_index.src.helper.check_file import is_parent_directory_exist


class BaseEeIndexPlotter:
    def calculate_er_values(self):
        raise NotImplementedError("Subclasses must implement this method")

    def calculate_edst_values(self):
        raise NotImplementedError("Subclasses must implement this method")

    def calculate_euel_values(self):
        raise NotImplementedError("Subclasses must implement this method")

    def calculate_ee_values(self):
        raise NotImplementedError("Subclasses must implement this method")

    def set_x_axis(self):
        raise NotImplementedError("Subclasses must implement this method")

    def customize_er_plot(self):
        raise NotImplementedError("Subclasses must implement this method")

    def customize_edst_plot(self):
        raise NotImplementedError("Subclasses must implement this method")

    def customize_euel_plot(self):
        raise NotImplementedError("Subclasses must implement this method")

    def customize_ee_plot(self):
        raise NotImplementedError("Subclasses must implement this method")

    def get_total_minutes(self):
        raise NotImplementedError("Subclasses must implement this method")

    def plot_er_figure(self, station, absolte_path):
        x_axis = self.set_x_axis()
        y_axis = self.calculate_er_values(station)
        fig, ax = plt.subplots()
        ax.plot(x_axis, y_axis)
        # x_interp, y_interp = self.interpolate(x_axis, y_axis)
        # y_smooth = self.smooth(y_interp)
        # fig, ax = plt.subplots()
        # ax.plot(x_interp, y_smooth)
        self.customize_er_plot(station, ax)
        self.save_figure(absolte_path)
        plt.close()

    def plot_edst_figure(self, absolte_path):
        x_axis = self.set_x_axis()
        y_axis = self.calculate_edst_values()
        x_interp, y_interp = self.interpolate(x_axis, y_axis)
        y_smooth = self.smooth(y_interp)
        fig, ax = plt.subplots()
        ax.plot(x_interp, y_smooth)
        self.customize_edst_plot(ax)
        self.save_figure(absolte_path)
        plt.close()

    def plot_euel_figure(self, station, absolte_path):
        x_axis = self.set_x_axis()
        y_axis = self.calculate_euel_values(station)
        x_interp, y_interp = self.interpolate(x_axis, y_axis)
        y_smooth = self.smooth(y_interp)
        fig, ax = plt.subplots()
        ax.plot(x_interp, y_smooth)
        self.customize_euel_plot(station, ax)
        self.save_figure(absolte_path)
        plt.close()

    def plot_ee_figure(self, station, absolute_path):
        x_axis = self.set_x_axis()
        fig, ax = plt.subplots()
        ee_valus = self.calculate_ee_values(station)
        er, edst, euel = ee_valus[0], ee_valus[1], ee_valus[2]
        ax.plot(x_axis, er, label="ER", color="black", lw=0.5)
        ax.plot(x_axis, edst, label="EDst", color="green", lw=0.5)
        ax.plot(x_axis, euel, label="EUEL", color="red", lw=0.5)
        # er_x_interp, er_interp = self.interpolate(x_axis, er)
        # edst_x_interp, edst_interp = self.interpolate(x_axis, edst)
        # euel_x_interp, euel_interp = self.interpolate(x_axis, euel)
        # er_smooth = self.smooth(er_interp)
        # edst_smooth = self.smooth(edst_interp)
        # euel_smooth = self.smooth(euel_interp)
        # ax.plot(er_x_interp, er_smooth, label="ER", color="black")
        # ax.plot(edst_x_interp, edst_smooth, label="EDst", color="green")
        # ax.plot(euel_x_interp, euel_smooth, label="EUEL", color="red")
        ax.legend()
        self.customize_ee_plot(station, ax)
        self.save_figure(absolute_path)
        plt.close()

    def interpolate(self, x_axis, y_axis):
        """Interpolate the nan values in the y_axis
        TODO:
            x_interpをオーバライドする必要がある
            エラーを出させる
        """
        nan_indices = np.isnan(y_axis)
        x_elements = self.get_total_minutes()
        x_interp = np.linspace(0, x_elements - 1, x_elements)
        y_interp = np.interp(x_interp, x_axis[~nan_indices], y_axis[~nan_indices])
        return x_interp, y_interp

    def smooth(self, y_axis):
        return savgol_filter(y_axis, Smooth.EE.length, Smooth.EE.deg)

    def show_figure(self):
        plt.show()

    def save_figure(self, absolte_path):
        if not is_parent_directory_exist(absolte_path):
            raise FileNotFoundError("Directory does not exist")
        plt.savefig(absolte_path)
        plt.clf()
