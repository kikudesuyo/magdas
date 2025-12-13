"""LTでのEE-indexのプロット"""

from datetime import timedelta

import matplotlib.pyplot as plt
import numpy as np
from src.dev.plot.axis import AxisConfigurator
from src.dev.plot.config import PlotConfigurator
from src.dev.plot.hover import HoverConfigurator
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParam
from src.service.calc_utils.moving_avg import calc_moving_avg
from src.service.ee_index.magdas_ee import MagdasEeService


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
        ee_service = MagdasEeService(ut_param)
        ee_data = ee_service.calc_all()
        euel_values = ee_data.euel
        # smoothed_euel = calc_moving_avg(
        #     euel_values, TimeUnit.ONE_HOUR.min, TimeUnit.THIRTY_MINUTES.min
        # )
        # x_axis = np.arange(0, len(smoothed_euel), 1)

        # self._plot_peak_point(
        #     x_axis[np.nanargmax(smoothed_euel)],
        #     np.nanmax(smoothed_euel),
        #     color="black",
        #     d=50,
        # )

        x_axis = np.arange(0, len(euel_values), 1)
        self.ax.plot(x_axis, euel_values, label=f"{station.code}_EUEL", color=color)

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

    anc = EeIndexStation.ANC
    hua = EeIndexStation.HUA
    eus = EeIndexStation.EUS

    start_dt = datetime(2017, 9, 14)
    end_dt = datetime(2018, 9, 14)

    for single_date in (
        start_dt + timedelta(n) for n in range((end_dt - start_dt).days + 1)
    ):
        p = Period(
            start=datetime.combine(single_date, datetime.min.time()),
            end=datetime.combine(single_date, datetime.min.time())
            + timedelta(days=1)
            - timedelta(minutes=1),
        )
        f = MagdasEdstService(p)
        edst = f.calc()

        max_kp = Kp().get_max_of_day(p)
        min_edst_val = np.min(edst)
        q = QuietDayDomain(min_edst=min_edst_val, max_kp=max_kp)

        if q.is_quiet_day():
            print(f"skip {single_date} (not quiet day)", max_kp, min_edst_val)
            continue
        p = LocalEeIndexPlotter(
            Period(
                start=single_date,
                end=single_date + timedelta(days=1) - timedelta(minutes=1),
            )
        )
        p.plot_euel(anc, "red")
        p.plot_euel(hua, "red")
        p.plot_euel(eus, "purple")
        p.set_title(f"EUEL ({single_date.strftime('%Y-%m-%d')})")
        p.show()
