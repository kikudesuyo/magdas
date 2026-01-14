"""LTでのEE-indexのプロット"""

from datetime import timedelta

import matplotlib.pyplot as plt
import numpy as np
from src.constants.time_relation import TimeUnit
from src.dev.plot.axis import AxisConfigurator
from src.dev.plot.config import PlotConfigurator
from src.dev.plot.hover import HoverConfigurator
from src.domain.magdas_station import EeIndexStation
from src.domain.region import Region
from src.domain.station_params import Period, StationParam
from src.service.calc_utils.moving_avg import calc_moving_avg
from src.service.ee_index.intermag_ee import IntermagEuelService
from src.service.ee_index.magdas_ee import MagdasEeService
from src.utils.path import generate_parent_abs_path


class LocalEeIndexPlotter:
    def __init__(self, lt_period: Period):
        self.lt_period = lt_period
        # self.factory = MagdasEeService()

        self.fig, self.ax = plt.subplots()

        PlotConfigurator(self.fig, self.ax).apply()
        HoverConfigurator(self.fig, self.ax, self.lt_period).apply()
        AxisConfigurator(self.ax, self.lt_period).apply()

    def plot_euel(self, station: EeIndexStation, color):
        ut_param = StationParam(station, self.lt_period).to_ut_params()
        # ee_service = MagdasEeService(ut_param)

        service = IntermagEuelService(ut_param, Region.BRAZIL)
        euel_data = service.get_euel_data_by_range()
        euel_values = euel_data.array

        # ee_data = ee_service.calc_all()
        # euel_values = ee_data.euel

        smoothed_euel = calc_moving_avg(
            euel_values, TimeUnit.ONE_HOUR.min, TimeUnit.THIRTY_MINUTES.min
        )
        x_axis = np.arange(0, len(smoothed_euel), 1)

        self._plot_peak_point(
            x_axis[np.nanargmax(smoothed_euel)],
            np.nanmax(smoothed_euel),
            color="black",
            d=50,
        )
        self.ax.plot(x_axis, smoothed_euel, label=f"{station.code}_EUEL", color=color)

    def _plot_peak_point(self, index, value, color, d):
        self.ax.plot(index, value, marker="o", markersize=5, color=color)
        self.ax.text(
            index + d, value + 5, f"{value:.2f}", fontsize=12, ha="center", color=color
        )

    def _draw_vertical_lines(self):
        for hour in [9, 15]:
            delta_minutes = (hour * 60) - (
                self.lt_period.start.hour * 60 + self.lt_period.start.minute
            )
            if 0 <= delta_minutes <= self.lt_period.total_minutes():
                self.ax.axvline(
                    x=delta_minutes,
                    color=(1.0, 0.0, 0.0, 0.3),
                    linestyle="--",
                    linewidth=2,
                )

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

    from src.domain.quiet import QuietDayDomain
    from src.domain.station_params import Period, StationParam
    from src.service.ee_index.magdas_ee import MagdasEdstService, MagdasEeService
    from src.service.kp import Kp
    from src.service.peculiar_eej import PeculiarEejService

    service = PeculiarEejService()
    data_list = service.get_by_region(Region.BRAZIL)

    for d in data_list:
        period = Period(
            start=datetime(d.date.year, d.date.month, d.date.day, 0, 0),
            end=datetime(d.date.year, d.date.month, d.date.day, 23, 59),
        )

        plotter = LocalEeIndexPlotter(period)

        plotter.plot_euel(EeIndexStation.EUS, "red")
        plotter.plot_euel(EeIndexStation.TTB, "blue")
        # plotter.plot_euel(EeIndexStation.KOU, "green")

        plotter.set_title("Brazil Region EUEL on " + d.date.strftime("%Y/%m/%d.date"))

        plotter.show()

        # path = generate_parent_abs_path(
        #     f"/img/peculiar_eej/brazil_region_by_kato/{d.type}/{d.date.strftime('%Y%m%d')}.png"
        # )
        # plotter.save(path)
