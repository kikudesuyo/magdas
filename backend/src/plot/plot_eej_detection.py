from datetime import time, timedelta
from typing import List

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backend_bases import MouseEvent
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period
from src.plot.config import PlotConfig
from src.service.calc_eej_detection import BestEuelSelectorForEej


class EejDetectionPlotter:
    def __init__(self, lt_period: Period):
        self.lt_period = lt_period
        PlotConfig.rcparams()
        self.fig, self.ax = plt.subplots()
        self._set_axis_labels()
        self.fig.canvas.mpl_connect("motion_notify_event", self._on_move)

    def _validate_period(self):
        if self.lt_period.start.time() != time(
            0, 0
        ) or self.lt_period.end.time() != time(23, 59):
            raise ValueError("start_lt must be 00:00 and end_lt must be 23:59.")

    def plot_euel_to_detect_eej(
        self, stations: List[EeIndexStation], color, is_dip: bool
    ):
        """EEJを検知するためのプロット
        注意:
        EEJの検知は日毎で行うため、start_ltとend_ltは日付の粒度で指定してください
        """
        self._validate_period()
        date_range = [
            self.lt_period.start.date() + timedelta(days=i)
            for i in range((self.lt_period.end - self.lt_period.start).days + 1)
        ]
        euel = np.hstack(
            [
                BestEuelSelectorForEej(stations, d, is_dip).select_euel_data().array
                for d in date_range
            ]
        )
        x_axis = np.arange(0, len(euel), 1)
        label = (
            f"{'dip' if is_dip else 'offdip'}({', '.join([s.code for s in stations])})"
        )
        self.ax.plot(x_axis, euel, label=label, color=color)

    def _set_axis_labels(self):
        data_length = self.lt_period.total_minutes() + 1
        self.ax.set_ylabel("nT", rotation=0)
        self.ax.set_xlim(0, data_length)
        self.ax.set_ylim(-100, 200)
        self.ax.set_xlabel("Local Time", fontsize=15)
        tick_interval = max(1, data_length // 8)
        ticks = range(0, data_length, tick_interval)
        time_labels = [
            (self.lt_period.start + timedelta(minutes=i)).strftime("%m/%d %H:%M")
            for i in ticks
        ]
        self.ax.set_xticks(ticks)
        self.ax.set_xticklabels(time_labels)

    def _on_move(self, event: MouseEvent):
        if not event.inaxes:
            return
        x, y = event.xdata, event.ydata
        if x is None or y is None:
            return
        minute_offset = int(x)
        current_time = self.lt_period.start + timedelta(minutes=minute_offset)
        time_str = current_time.strftime("%Y/%m/%d %H:%M")
        self.ax.set_title(f"Date: {time_str}, Value: {y:.2f}")
        self.ax.figure.canvas.draw()

    def set_title(self, title):
        self.ax.set_title(title, fontsize=15, fontweight="semibold", pad=10)

    def show(self):
        self.ax.legend(loc="lower left", fontsize=18)
        plt.show()

    def save(self, path):
        self.ax.legend(loc="lower left", fontsize=18)
        plt.savefig(path)
        plt.close(self.fig)


if __name__ == "__main__":
    from datetime import datetime

    from src.domain.magdas_station import EeIndexStation
    from src.domain.station_params import Period

    dip_stations = [EeIndexStation.ANC, EeIndexStation.HUA]
    offdip_stations = [EeIndexStation.EUS]

    date = datetime(2017, 2, 7, 0, 0)

    lt_period = Period(start=date, end=date + timedelta(days=1) - timedelta(minutes=1))
    plotter = EejDetectionPlotter(lt_period)
    plotter.plot_euel_to_detect_eej(dip_stations, color="red", is_dip=True)
    plotter.plot_euel_to_detect_eej(offdip_stations, color="blue", is_dip=False)
    plotter.show()
