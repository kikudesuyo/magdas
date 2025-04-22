from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
from src.service.dst import get_dst_values
from src.service.ee_index.calc.edst import Edst
from src.service.ee_index.calc.er import Er
from src.service.ee_index.calc.euel import create_euel
from src.service.ee_index.calc.h_component_extraction import HComponent
from src.service.ee_index.calc.moving_ave import calc_moving_avg
from src.service.ee_index.constant.magdas_station import EeIndexStation
from src.service.ee_index.constant.time_relation import Sec
from src.service.ee_index.helper.params import CalcParams, Period
from src.service.ee_index.plot.config import PlotConfig


class EeIndexPlotter:
    def __init__(self, start_ut: datetime, end_ut: datetime):
        self.start_ut = start_ut
        self.end_ut = end_ut
        self.period = Period(start_ut, end_ut)
        PlotConfig.rcparams()
        self.fig, self.ax = plt.subplots()
        self._set_axis_labels()
        self.fig.canvas.mpl_connect("motion_notify_event", self._on_move)
        self.ax.text(
            0.5,
            0.95,
            "",
            transform=self.ax.transAxes,
            ha="center",
            va="center",
            fontsize=12,
            color="black",
        )

    def plot_er(self, station, color):
        params = CalcParams(station, self.period)
        h = HComponent(params)
        er_values = Er(h).calc_er()
        x_axis, y_axis = np.arange(0, len(er_values), 1), er_values
        self.ax.plot(x_axis, y_axis, label="ER", color=color)

    def plot_edst(self):
        edst = Edst(self.period).compute_smoothed_edst()
        x_axis, y_axis = np.arange(0, len(edst), 1), edst
        self.ax.plot(x_axis, y_axis, label="EDst", color="green", lw=1.3)

    def plot_euel(self, station, color):
        p = CalcParams(station, self.period)
        euel = create_euel(p)
        euel_values = euel.calc_euel()
        smoothed_euel = calc_moving_avg(euel_values, 120, 60)
        x_axis = np.arange(0, len(smoothed_euel), 1)
        self.ax.plot(x_axis, smoothed_euel, label=f"{station}_EUEL", color=color)

    # def plot_dst(self, color):
    #     dst = get_dst_values(self.start_date, self.end_date)
    #     dst_interpolated = np.repeat(dst, 60)
    #     x_axis = np.arange(0, len(dst_interpolated), 1)
    #     self.ax.plot(x_axis, dst_interpolated, label="Dst", color=color, lw=1.3)

    def plot_ee(self, station):
        # TODO: 各インデックスの宣言においてパフォーマンス改善の余地あり
        params = CalcParams(station, self.period)
        h = HComponent(params)
        er = Er(h)
        edst = Edst(self.period)
        euel = create_euel(params)
        er_values = er.calc_er()
        edst_values = edst.compute_smoothed_edst()
        euel_values = euel.calc_euel()
        if len(er_values) != len(edst_values) or len(er_values) != len(euel_values):
            raise ValueError("The length of the arrays must be the same")
        x_axis = np.arange(0, len(er_values), 1)
        self.ax.plot(x_axis, er, label="ER", color="black", lw=0.5)
        self.ax.plot(x_axis, edst, label="EDst", color="green", lw=0.5)
        self.ax.plot(x_axis, euel, label="EUEL", color="red", lw=0.5)

    def _set_axis_labels(self):
        data_length = (
            int((self.end_ut - self.start_ut).total_seconds()) // Sec.ONE_MINUTE.const
            + 1
        )
        self.ax.set_ylabel("nT", rotation=0)
        self.ax.set_xlim(0, data_length)
        self.ax.set_ylim(-100, 200)
        self.ax.set_xlabel("UT", fontsize=15)
        tick_interval = max(1, data_length // 8)
        ticks = range(0, data_length, tick_interval)
        time_labels = [
            (self.start_ut + timedelta(minutes=i)).strftime("%m/%d %H:%M")
            for i in ticks
        ]
        self.ax.set_xticks(ticks)
        self.ax.set_xticklabels(time_labels)

    def _on_move(self, event):
        if not event.inaxes:
            return
        x, y = event.xdata, event.ydata
        time_str = (self.start_ut + timedelta(minutes=int(x))).strftime("%m/%d %H:%M")
        self.ax.set_title(f"Time: {time_str}, Value: {y:.2f}")
        self.ax.figure.canvas.draw()

    def set_title(self, title):
        self.ax.set_title(title, fontsize=15, fontweight="semibold", pad=10)

    def show(self):
        self.ax.legend(loc="lower left", fontsize=18)
        plt.draw()
        plt.show()

    def save(self, path):
        """画像保存

        Caution:
            show後に呼び出すと白い画面が表示される
        """
        self.ax.legend(loc="lower left", fontsize=18)
        plt.savefig(path)


if __name__ == "__main__":
    start_date = datetime(2014, 1, 1, 0, 0)
    end_date = datetime(2014, 1, 31, 23, 59)

    anc = EeIndexStation.ANC
    eus = EeIndexStation.EUS
    p = EeIndexPlotter(start_date, end_date)
    p.plot_er(anc, "blue")
    p.plot_er(eus, "red")
    p.plot_edst()
    p.show()
