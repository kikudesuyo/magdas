from datetime import timedelta

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backend_bases import MouseEvent
from src.constants.time_relation import TimeUnit
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParam
from src.plot.config import PlotConfig
from src.service.ee_index.factory_ee import EeFactory
from src.service.moving_avg import calc_moving_avg


class EeIndexPlotter:
    def __init__(self, ut_period: Period):
        self.ut_period = ut_period
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

    def plot_er(self, station: EeIndexStation, color):
        er = self.factory.create_er(StationParam(station, self.ut_period))
        er_values = er.calc_er()
        x_axis, y_axis = np.arange(0, len(er_values), 1), er_values
        self.ax.plot(x_axis, y_axis, label=f"{station.code}_ER", color=color)

    def plot_edst(self):
        edst = self.factory.create_edst(self.ut_period)
        edst_raw = edst.calc_edst()
        edst_values = calc_moving_avg(
            edst_raw, TimeUnit.ONE_HOUR.min, TimeUnit.THIRTY_MINUTES.min
        )
        x_axis, y_axis = np.arange(0, len(edst_values), 1), edst_values
        self.ax.plot(x_axis, y_axis, label="EDst", color="green", lw=1.3)

    def plot_euel(self, station: EeIndexStation, color):
        p = StationParam(station, self.ut_period)
        euel = self.factory.create_euel(p)
        euel_values = euel.calc_euel()
        # smoothed_euel = calc_moving_avg(
        #     euel_values, TimeUnit.TWO_HOURS.min, TimeUnit.ONE_HOUR.min
        # )
        smoothed_euel = euel_values
        x_axis = np.arange(0, len(smoothed_euel), 1)
        self.ax.plot(x_axis, smoothed_euel, label=f"{station.code}_EUEL", color=color)

    def plot_ee(self, station: EeIndexStation):
        params = StationParam(station, self.ut_period)
        er = self.factory.create_er(params)
        edst = self.factory.create_edst(self.ut_period)
        euel = self.factory.create_euel(params)
        er_values = er.calc_er()
        edst_raw = edst.calc_edst()
        edst_values = calc_moving_avg(
            edst_raw, TimeUnit.ONE_HOUR.min, TimeUnit.THIRTY_MINUTES.min
        )
        euel_values = euel.calc_euel()
        if len(er_values) != len(edst_values) or len(er_values) != len(euel_values):
            raise ValueError("The length of the arrays must be the same")
        x_axis = np.arange(0, len(er_values), 1)
        self.ax.plot(x_axis, er_values, label="ER", color="black", lw=0.5)
        self.ax.plot(x_axis, edst_values, label="EDst", color="green", lw=0.5)
        self.ax.plot(x_axis, euel_values, label="EUEL", color="red", lw=0.5)

    def _set_axis_labels(self):
        data_length = self.ut_period.total_minutes() + 1
        self.ax.set_ylabel("nT", rotation=0)
        self.ax.set_xlim(0, data_length)
        self.ax.set_ylim(-100, 200)
        self.ax.set_xlabel("UT", fontsize=15)
        tick_interval = max(1, data_length // 8)
        ticks = range(0, data_length, tick_interval)
        time_labels = [
            (self.ut_period.start + timedelta(minutes=i)).strftime("%m/%d %H:%M")
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
        current_time = self.ut_period.start + timedelta(minutes=minute_offset)
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

    from src.domain.station_params import Period, StationParam

    anc = EeIndexStation.ANC
    hua = EeIndexStation.HUA
    eus = EeIndexStation.EUS
    dav = EeIndexStation.DAV
    lkw = EeIndexStation.LKW

    # date = datetime(2016, 2, 6, 0, 0)
    date = datetime(2018, 12, 16, 0, 0)
    ut_period = Period(start=date, end=date + timedelta(days=7) - timedelta(minutes=1))
    p = EeIndexPlotter(ut_period)
    p.plot_euel(anc, "red")
    p.plot_euel(hua, "red")
    p.plot_euel(eus, "purple")

    p.plot_euel(dav, "orange")
    p.plot_euel(lkw, "green")

    # p.plot_edst()
    p.show()
