from datetime import datetime, time, timedelta

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backend_bases import MouseEvent
from src.constants.time_relation import TimeUnit
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParams
from src.usecase.ee_index.calc_eej_detection import calc_euel_for_eej_detection
from src.usecase.ee_index.calc_moving_avg import calc_moving_avg
from src.usecase.ee_index.factory_ee import EeFactory
from src.usecase.ee_index.plot_config import PlotConfig


class EejDetectionPlotter:
    def __init__(self, lt_period: Period):
        self.lt_period = lt_period
        PlotConfig.rcparams()
        self.fig, self.ax = plt.subplots()
        self._set_axis_labels()
        self.fig.canvas.mpl_connect("motion_notify_event", self._on_move)

    def plot_local_euel(self, station: EeIndexStation):
        params = StationParams(station, self.lt_period)
        ut_params = params.to_ut_params()
        factory = EeFactory()
        euel = factory.create_euel(ut_params)
        raw_euel = euel.calc_euel()
        euel_values = calc_moving_avg(
            raw_euel, TimeUnit.TWO_HOURS.min, TimeUnit.ONE_HOUR.min
        )
        x_axis = np.arange(0, len(euel_values), 1)
        self.ax.plot(x_axis, euel_values, label=station.name)

    def plot_euel_to_detect_eej(self, station: EeIndexStation, color):
        """EEJを検知するためのプロット
        注意:
        EEJの検知は日毎で行うため、start_ltとend_ltは日付の粒度で指定してください
        """
        if self.lt_period.start.time() != time(
            0, 0
        ) or self.lt_period.end.time() != time(23, 59):
            raise ValueError("start_lt must be 00:00 and end_lt must be 23:59.")
        date_range = [
            self.lt_period.start.date() + timedelta(days=i)
            for i in range((self.lt_period.end - self.lt_period.start).days + 1)
        ]
        euel = np.hstack([calc_euel_for_eej_detection(station, d) for d in date_range])
        x_axis = np.arange(0, len(euel), 1)
        self.ax.plot(x_axis, euel, label=station.name, color=color)

    def plot_pure_euel(self, station: EeIndexStation, color):
        lt_params = StationParams(station, self.lt_period)
        ut_params = lt_params.to_ut_params()
        factory = EeFactory()
        euel = factory.create_euel(ut_params)
        euel_values = euel.calc_euel()
        x_axis = np.arange(0, len(euel_values), 1)
        self.ax.plot(x_axis, euel_values, label=station.name, color=color)

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
        time_str = (self.lt_period.start + timedelta(minutes=int(x))).strftime(
            "%m/%d %H:%M"
        )
        self.ax.set_title(f"Time: {time_str}, Value: {y:.2f}")
        self.ax.figure.canvas.draw()

    def show(self):
        self.ax.legend(loc="lower left", fontsize=18)
        plt.show()

    def save(self, path):
        self.ax.legend(loc="lower left", fontsize=18)
        plt.savefig(path)


if __name__ == "__main__":
    lt_period = Period(
        start=datetime(2014, 1, 1, 0, 0),
        end=datetime(2014, 1, 31, 23, 59),
    )
    detection = EejDetectionPlotter(lt_period)
    detection.plot_euel_to_detect_eej(EeIndexStation.ANC, "red")
    detection.plot_euel_to_detect_eej(EeIndexStation.EUS, "purple")
    detection.show()
