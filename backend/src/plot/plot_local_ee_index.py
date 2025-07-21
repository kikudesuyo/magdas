from datetime import timedelta

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backend_bases import MouseEvent
from src.constants.time_relation import TimeUnit
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParams
from src.plot.config import PlotConfig
from src.service.ee_index.factory_ee import EeFactory
from src.service.moving_avg import calc_moving_avg


class LocalEeIndexPlotter:
    def __init__(self, lt_period: Period):
        self.lt_period = lt_period
        self.factory = EeFactory()

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

    def plot_euel(self, station: EeIndexStation, color):
        ut_param = StationParams(station, self.lt_period).to_ut_params()
        euel = self.factory.create_euel(ut_param)
        euel_values = euel.calc_euel()
        smoothed_euel = calc_moving_avg(
            euel_values, TimeUnit.ONE_HOUR.min, TimeUnit.THIRTY_MINUTES.min
        )
        x_axis = np.arange(0, len(smoothed_euel), 1)
        self.ax.plot(x_axis, smoothed_euel, label=f"{station.code}_EUEL", color=color)

    def _set_axis_labels(self):
        data_length = self.lt_period.total_minutes() + 1
        self.ax.set_ylabel("nT", rotation=0)
        self.ax.set_xlim(0, data_length)
        self.ax.set_ylim(-100, 200)
        self.ax.set_xlabel("UT", fontsize=15)
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
        plt.draw()
        plt.show()

    def save(self, path):
        """画像保存

        Caution:
            show後に呼び出すと白い画面が表示される
        """
        self.ax.legend(loc="lower left", fontsize=12)
        plt.savefig(path)
        plt.close(self.fig)


if __name__ == "__main__":
    from datetime import datetime

    from src.domain.station_params import Period, StationParams

    anc = EeIndexStation.ANC
    # hua = EeIndexStation.HUA
    eus = EeIndexStation.EUS

    date = datetime(2020, 10, 10, 0, 0)
    lt_period = Period(start=date, end=date + timedelta(days=1) - timedelta(minutes=1))
    p = LocalEeIndexPlotter(lt_period)
    p.plot_euel(anc, "red")
    # p.plot_euel(hua, "red")
    p.plot_euel(eus, "purple")

    p.show()
