"""EEJ検知のためのプロット"""

from datetime import time, timedelta
from typing import List

import numpy as np
from matplotlib import pyplot as plt
from src.dev.plot.config import PlotConfig
from src.dev.plot.hover import HoverController
from src.domain.magdas_station import EeIndexStation
from src.domain.region import Region
from src.domain.station_params import Period
from src.service.eej.best_euel_selector import BestEuelSelectorFactory


class EejDetectionPlotter:
    def __init__(self, lt_period: Period):
        self.lt_period = lt_period
        PlotConfig.rcparams()
        self.fig, self.ax = plt.subplots()
        self._set_axis_labels()
        HoverController(self.fig, self.ax, self.lt_period)

    def _validate_period(self):
        if self.lt_period.start.time() != time(
            0, 0
        ) or self.lt_period.end.time() != time(23, 59):
            raise ValueError("start_lt must be 00:00 and end_lt must be 23:59.")

    def plot_euel_to_detect_eej(
        self, region: Region, stations: List[EeIndexStation], color, is_dip: bool
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
                BestEuelSelectorFactory()
                .create(region, stations, d, is_dip)
                .select_best_euel_data()
                .array
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

    region = Region.SOUTH_AMERICA

    dip_stations = [EeIndexStation.ANC, EeIndexStation.HUA]
    offdip_stations = [EeIndexStation.EUS]

    start_date = datetime(2017, 2, 1, 0, 0)
    end_date = datetime(2017, 2, 28, 23, 59)

    current_date = start_date
    while current_date <= end_date:
        lt_period = Period(
            start=current_date,
            end=current_date + timedelta(days=1) - timedelta(minutes=1),
        )
        plotter = EejDetectionPlotter(lt_period)
        plotter.plot_euel_to_detect_eej(region, dip_stations, color="red", is_dip=True)
        plotter.plot_euel_to_detect_eej(
            region, offdip_stations, color="blue", is_dip=False
        )
        plotter.set_title(f"EEJ Detection Plot for {current_date.strftime('%Y-%m-%d')}")
        # plotter.show()
        plotter.save(f"refactor/eej_detection_{current_date.strftime('%Y%m%d')}.png")
        current_date += timedelta(days=1)
