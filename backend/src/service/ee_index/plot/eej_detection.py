from datetime import datetime, timedelta

import numpy as np
from matplotlib import pyplot as plt
from src.service.ee_index.calc.euel_index import get_local_euel
from src.service.ee_index.calc.moving_ave import calc_moving_ave
from src.service.ee_index.constant.magdas_station import EeIndexStation
from src.service.ee_index.constant.time_relation import Sec
from src.service.ee_index.plot.config import PlotConfig


class EejDetectionPlotter:
    def __init__(self, start_lt: datetime, end_lt: datetime):
        self.start_lt = start_lt
        self.end_lt = end_lt
        PlotConfig.rcparams()
        self.fig, self.ax = plt.subplots()
        self._set_axis_labels()
        self.fig.canvas.mpl_connect("motion_notify_event", self._on_move)

    def plot_local_euel(self, station: EeIndexStation):
        local_euel = get_local_euel(station, self.start_lt, self.end_lt)
        moving_avg = calc_moving_ave(local_euel, 120, 60)
        x_axis = np.arange(0, len(moving_avg), 1)
        self.ax.plot(x_axis, moving_avg, label=station.name)

    def plot_pure(self, station: EeIndexStation):
        local_euel = get_local_euel(station, self.start_lt, self.end_lt)
        x_axis = np.arange(0, len(local_euel), 1)
        self.ax.plot(x_axis, local_euel, label=station.name)

    def _set_axis_labels(self):
        data_length = (
            int((self.end_lt - self.start_lt).total_seconds()) // Sec.ONE_MINUTE.const
            + 1
        )
        self.ax.set_ylabel("nT", rotation=0)
        self.ax.set_xlim(0, data_length)
        self.ax.set_ylim(-100, 200)
        self.ax.set_xlabel("Local Time", fontsize=15)
        tick_interval = max(1, data_length // 8)
        ticks = range(0, data_length, tick_interval)
        time_labels = [
            (self.start_lt + timedelta(minutes=i)).strftime("%m/%d %H:%M")
            for i in ticks
        ]
        self.ax.set_xticks(ticks)
        self.ax.set_xticklabels(time_labels)

    def _on_move(self, event):
        if not event.inaxes:
            return
        x, y = event.xdata, event.ydata
        time_str = (self.start_lt + timedelta(minutes=int(x))).strftime("%m/%d %H:%M")
        self.ax.set_title(f"Time: {time_str}, Value: {y:.2f}")
        self.ax.figure.canvas.draw()

    def show(self):
        self.ax.legend(loc="lower left", fontsize=18)
        plt.show()

    def save(self, path):
        self.ax.legend(loc="lower left", fontsize=18)
        plt.savefig(path)


start_lt = datetime(2014, 1, 20, 0, 0)
end_lt = datetime(2014, 1, 20, 23, 59)
detection = EejDetectionPlotter(start_lt, end_lt)
detection.plot_local_euel(EeIndexStation.ANC)
detection.plot_local_euel(EeIndexStation.EUS)
detection.plot_pure(EeIndexStation.ANC)
detection.plot_pure(EeIndexStation.EUS)
detection.show()
