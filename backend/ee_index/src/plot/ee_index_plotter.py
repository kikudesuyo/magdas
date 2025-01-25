from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
from ee_index.src.calc.edst_index import Edst
from ee_index.src.calc.er_value import Er
from ee_index.src.calc.euel_index import Euel
from ee_index.src.constant.time_relation import Min


class EeIndexPlotter:
    def __init__(self, start_date: datetime, end_date: datetime):
        self.start_datetime = start_date
        self.days = (end_date - start_date).days + 1
        self.fig, self.ax = plt.subplots()

    def plot_er(self, station):
        er = Er(station, self.start_datetime).calc_er_for_days(self.days)
        x_axis, y_axis = np.arange(0, len(er), 1), er
        self.ax.plot(x_axis, y_axis)
        self.ax.set_title(
            f"{self.start_datetime.date()}_{station}_UT",
            loc="center",
            fontsize=12,
            fontweight="bold",
        )
        self._set_axis_labels("ER Value(nT)", self.start_datetime, len(er))

    def plot_edst(self):
        edst = Edst.compute_smoothed_edst(self.start_datetime, self.days)
        x_axis, y_axis = np.arange(0, len(edst), 1), edst
        self.ax.plot(x_axis, y_axis)
        self.ax.set_title(
            f"{self.start_datetime.date()}_UT",
            loc="center",
            fontsize=12,
            fontweight="bold",
        )
        self._set_axis_labels("EDst Value(nT)", self.start_datetime, len(edst))

    def plot_euel(self, station):
        euel = Euel.calculate_euel_for_days(station, self.start_datetime, self.days)
        x_axis, y_axis = np.arange(0, len(euel), 1), euel
        self.ax.plot(x_axis, y_axis)
        self.ax.set_title(
            f"{self.start_datetime.date()}_{station}_UT",
            loc="center",
            fontsize=12,
            fontweight="bold",
        )
        self._set_axis_labels("EUEL Value(nT)", self.start_datetime, len(euel))

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
        self.ax.set_title(
            f"{self.start_datetime.date()}_{station}_UT",
            loc="center",
            fontsize=12,
            fontweight="bold",
        )
        self._set_axis_labels("EEindex Value(nT)", self.start_datetime, len(er))

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

    def show(self):
        plt.show()

    def save(self, path):
        """画像保存

        Caution:
            show後に呼び出すと白い画面が表示される
        """
        plt.savefig(path)
