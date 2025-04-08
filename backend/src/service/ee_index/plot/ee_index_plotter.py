from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
from src.service.dst.dst_data import get_dst_values
from src.service.ee_index.calc.edst_index import Edst
from src.service.ee_index.calc.er_value import Er
from src.service.ee_index.calc.euel_index import Euel
from src.service.ee_index.calc.moving_ave import calc_moving_ave
from src.service.ee_index.constant.time_relation import Sec
from src.service.ee_index.plot.config import PlotConfig


class EeIndexPlotter:
    def __init__(self, start_dt: datetime, end_dt: datetime):
        self.start_dt = start_dt
        self.end_dt = end_dt
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

    def plot_er(self, station):
        er = Er(station, self.start_dt, self.end_dt).calc_er()
        x_axis, y_axis = np.arange(0, len(er), 1), er
        self.ax.plot(x_axis, y_axis, label="ER", color="black", lw=1.3)

    def plot_edst(self):
        edst = Edst.compute_smoothed_edst(self.start_dt, self.end_dt)
        x_axis, y_axis = np.arange(0, len(edst), 1), edst
        self.ax.plot(x_axis, y_axis, label="EDst", color="green", lw=1.3)

    def plot_euel(self, station, color):
        euel = Euel.calc_euel(station, self.start_dt, self.end_dt)
        smoothed_euel = calc_moving_ave(euel, 120, 60)
        x_axis = np.arange(0, len(smoothed_euel), 1)
        self.ax.plot(
            x_axis, smoothed_euel, label=f"{station}_EUEL", color=color, lw=1.3
        )

    # def plot_dst(self, color):
    #     dst = get_dst_values(self.start_date, self.end_date)
    #     dst_interpolated = np.repeat(dst, 60)
    #     x_axis = np.arange(0, len(dst_interpolated), 1)
    #     self.ax.plot(x_axis, dst_interpolated, label="Dst", color=color, lw=1.3)

    def plot_ee(self, station):
        er = Er(station, self.start_dt, self.end_dt).calc_er()
        edst = Edst.compute_smoothed_edst(self.start_dt, self.end_dt)
        euel = Euel.calc_euel(station, self.start_dt, self.end_dt)
        if len(er) != len(edst) or len(er) != len(euel):
            raise ValueError("The length of the arrays must be the same")
        x_axis = np.arange(0, len(er), 1)
        self.ax.plot(x_axis, er, label="ER", color="black", lw=0.5)
        self.ax.plot(x_axis, edst, label="EDst", color="green", lw=0.5)
        self.ax.plot(x_axis, euel, label="EUEL", color="red", lw=0.5)

    def _set_axis_labels(self):
        data_length = (
            int((self.end_dt - self.start_dt).total_seconds()) // Sec.ONE_MINUTE.const
            + 1
        )
        self.ax.set_ylabel("nT", rotation=0)
        self.ax.set_xlim(0, data_length)
        self.ax.set_ylim(-100, 200)
        self.ax.set_xlabel("UT", fontsize=15)
        tick_interval = max(1, data_length // 8)
        ticks = range(0, data_length, tick_interval)
        time_labels = [
            (self.start_dt + timedelta(minutes=i)).strftime("%m/%d %H:%M")
            for i in ticks
        ]
        self.ax.set_xticks(ticks)
        self.ax.set_xticklabels(time_labels)

    def _on_move(self, event):
        if not event.inaxes:
            return
        x, y = event.xdata, event.ydata
        time_str = (self.start_dt + timedelta(minutes=int(x))).strftime("%m/%d %H:%M")
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


p = EeIndexPlotter(datetime(2014, 1, 1, 0, 0), datetime(2014, 1, 10, 23, 59))
p.plot_euel("DAV", "red")
p.plot_euel("EUS", "blue")
p.show()
# p.plot_er("kakioka")
