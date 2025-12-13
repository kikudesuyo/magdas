"""EE-indexのプロット"""

from datetime import timedelta

import matplotlib.pyplot as plt
import numpy as np
from src.constants.time_relation import TimeUnit
from src.dev.plot.axis import AxisConfigurator
from src.dev.plot.config import PlotConfigurator
from src.dev.plot.hover import HoverConfigurator
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParam
from src.service.calc_utils.moving_avg import calc_moving_avg
from src.service.ee_index.magdas_ee import (
    MagdasEdstService,
    MagdasEeService,
    MagdasErService,
    MagdasEuelService,
)


class EeIndexPlotter:
    def __init__(self, ut_period: Period):
        self.ut_period = ut_period
        # self.factory = MagdasEeFactory()

        self.fig, self.ax = plt.subplots()
        PlotConfigurator(self.fig, self.ax).apply()
        HoverConfigurator(self.fig, self.ax, self.ut_period).apply()
        AxisConfigurator(self.ax, self.ut_period).apply()

    def plot_er(self, station: EeIndexStation, color):
        er = MagdasErService(StationParam(station, self.ut_period))
        er_values = er.calc()
        x_axis, y_axis = np.arange(0, len(er_values), 1), er_values
        self.ax.plot(x_axis, y_axis, label=f"{station.code}_ER", color=color)

    def plot_edst(self):
        edst = MagdasEdstService(self.ut_period)
        edst_raw = edst.calc()
        edst_values = calc_moving_avg(
            edst_raw, TimeUnit.ONE_HOUR.min, TimeUnit.THIRTY_MINUTES.min
        )
        x_axis, y_axis = np.arange(0, len(edst_values), 1), edst_values
        self.ax.plot(x_axis, y_axis, label="EDst", color="green", lw=1.3)

    def plot_euel(self, station: EeIndexStation, color):
        p = StationParam(station, self.ut_period)
        euel = MagdasEuelService(p)
        euel_values = euel.calc()
        # smoothed_euel = calc_moving_avg(
        #     euel_values, TimeUnit.TWO_HOURS.min, TimeUnit.ONE_HOUR.min
        # )
        smoothed_euel = euel_values
        x_axis = np.arange(0, len(smoothed_euel), 1)
        self.ax.plot(x_axis, smoothed_euel, label=f"{station.code}_EUEL", color=color)

    def plot_ee(self, station: EeIndexStation):
        params = StationParam(station, self.ut_period)
        ee_service = MagdasEeService(params)
        ee_data = ee_service.calc_all()

        edst_values = calc_moving_avg(
            ee_data.edst, TimeUnit.ONE_HOUR.min, TimeUnit.THIRTY_MINUTES.min
        )
        euel_values = ee_data.euel
        if len(ee_data.er) != len(edst_values) or len(ee_data.er) != len(euel_values):
            raise ValueError("The length of the arrays must be the same")
        x_axis = np.arange(0, len(ee_data.er), 1)
        self.ax.plot(x_axis, ee_data.er, label="ER", color="black", lw=0.5)
        self.ax.plot(x_axis, edst_values, label="EDst", color="green", lw=0.5)
        self.ax.plot(x_axis, euel_values, label="EUEL", color="red", lw=0.5)

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
