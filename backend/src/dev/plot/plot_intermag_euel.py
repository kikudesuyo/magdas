"""加藤さんからいただいたデータからEUELのプロット"""

from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
from src.dev.plot.axis import AxisConfigurator
from src.dev.plot.config import PlotConfigurator
from src.dev.plot.hover import HoverConfigurator
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParam
from src.service.ee_index.intermag_ee import IntermagEuelService
from src.service.peculiar_eej import PeculiarEejService


class KatoEuelPlotter:
    # ===== Style 定数 =====
    FIG_SIZE = (15, 8)

    TITLE_FONT_SIZE = 15
    LABEL_FONT_SIZE = 12
    TICK_FONT_SIZE = 10

    Y_LIM_MIN = -150
    Y_LIM_MAX = 150

    LEGEND_FONT_SIZE = 12

    def __init__(self, ut_period: Period):
        self.ut_period = ut_period

        # PlotConfig.rcparams()

        self.fig, self.ax = plt.subplots(figsize=self.FIG_SIZE)
        PlotConfigurator(self.fig, self.ax).apply()
        HoverConfigurator(self.fig, self.ax, self.ut_period).apply()
        AxisConfigurator(self.ax, self.ut_period).apply()

    def plot_euel(self, station: EeIndexStation, color: str) -> None:
        service = IntermagEuelService(
            StationParam(station=station, period=self.ut_period)
        )
        data = service.get_euel_data_by_range()

        if not data:
            print(f"No data for {station.code}")
            return

        x = np.arange(len(data))
        y = np.array(data, dtype=float)

        self.ax.plot(
            x,
            y,
            label=f"{station.code}_EUEL",
            color=color,
            linewidth=0.8,
        )

    @staticmethod
    def _calc_tick_interval(length: int) -> int:
        return max(1, length // 10)

    def set_title(self, title: str) -> None:
        self.ax.set_title(
            title,
            fontsize=self.TITLE_FONT_SIZE,
            fontweight="semibold",
            pad=20,
        )

    def show(self) -> None:
        self.ax.legend(loc="lower left", fontsize=self.LEGEND_FONT_SIZE)
        plt.show()
        plt.close(self.fig)

    def save(self, path: str) -> None:
        self.ax.legend(loc="lower left", fontsize=self.LEGEND_FONT_SIZE)
        self.fig.savefig(path, dpi=300)


if __name__ == "__main__":

    from src.domain.region import Region
    from src.utils.path import generate_parent_abs_path

    service = PeculiarEejService()
    data_list = service.get_by_region(Region.BRAZIL)

    peculiar_eej_dates = [d.date for d in data_list]
    print(f"Peculiar EEJ dates in Brazil region: {peculiar_eej_dates}")

    for d in peculiar_eej_dates:
        period = Period(
            start=datetime(d.year, d.month, d.day, 0, 0),
            end=datetime(d.year, d.month, d.day, 23, 59),
        )

        plotter = KatoEuelPlotter(period)

        plotter.plot_euel(EeIndexStation.EUS, "red")
        plotter.plot_euel(EeIndexStation.TTB, "blue")
        plotter.plot_euel(EeIndexStation.KOU, "green")

        plotter.set_title("Brazil Region EUEL on " + d.strftime("%Y/%m/%d"))

        plotter.show()

        # out_path = generate_parent_abs_path(
        #     f"/img/peculiar_eej/brazil_region_by_kato/{d.strftime('%Y%m%d')}.png"
        # )
        # plotter.save(out_path)
