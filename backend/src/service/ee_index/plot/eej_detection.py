from datetime import datetime, time, timedelta

import numpy as np
from matplotlib import pyplot as plt
from src.service.ee_index.calc.detect_eej import calc_euel_for_eej_detection
from src.service.ee_index.calc.euel_index import EuelLt
from src.service.ee_index.calc.moving_ave import calc_moving_avg
from src.service.ee_index.calc.params import CalcParams, Period
from src.service.ee_index.constant.magdas_station import EeIndexStation
from src.service.ee_index.constant.time_relation import Sec
from src.service.ee_index.plot.config import PlotConfig


class EejDetectionPlotter:
    def __init__(self, start_lt: datetime, end_lt: datetime):
        if start_lt >= end_lt:
            raise ValueError("start_lt must be less than end_lt.")
        self.start_lt = start_lt
        self.end_lt = end_lt
        self.period = Period(start_lt, end_lt)

        PlotConfig.rcparams()
        self.fig, self.ax = plt.subplots()
        self._set_axis_labels()
        self.fig.canvas.mpl_connect("motion_notify_event", self._on_move)

    def plot_local_euel(self, station: EeIndexStation):
        p = CalcParams(station, self.period)
        euel_lt = EuelLt(p)
        moving_avg = calc_moving_avg(euel_lt.euel_values, 120, 60)
        x_axis = np.arange(0, len(moving_avg), 1)
        self.ax.plot(x_axis, moving_avg, label=station.name)

    def plot_euel_to_detect_eej(self, station: EeIndexStation, color):
        """EEJを検知するためのプロット
        注意:
        EEJの検知は日毎で行うため、start_ltとend_ltは日付の粒度で指定してください
        """
        if self.start_lt.time() != time(0, 0) or self.end_lt.time() != time(23, 59):
            raise ValueError("start_lt must be 00:00 and end_lt must be 23:59.")
        date_range = [
            self.start_lt.date() + timedelta(days=i)
            for i in range((self.end_lt - self.start_lt).days + 1)
        ]
        euel = np.hstack([calc_euel_for_eej_detection(station, d) for d in date_range])
        x_axis = np.arange(0, len(euel), 1)
        self.ax.plot(x_axis, euel, label=station.name, color=color)

    def plot_pure(self, station: EeIndexStation, color):
        p = CalcParams(station, self.period)
        euel_lt = EuelLt(p)
        x_axis = np.arange(0, len(euel_lt.euel_values), 1)
        self.ax.plot(x_axis, euel_lt.euel_values, label=station.name, color=color)

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


if __name__ == "__main__":
    start_date = datetime(2018, 1, 10, 0, 0)
    end_date = datetime(2018, 1, 31, 23, 59)
    detection = EejDetectionPlotter(start_date, end_date)
    # detection.plot_local_euel(EeIndexStation.ANC)
    # detection.plot_local_euel(EeIndexStation.EUS)
    detection.plot_euel_to_detect_eej(EeIndexStation.ANC, "red")
    detection.plot_euel_to_detect_eej(EeIndexStation.EUS, "purple")
    detection.show()
