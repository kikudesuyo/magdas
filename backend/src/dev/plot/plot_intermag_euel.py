"""加藤さんからいただいたデータからEUELのプロット"""

from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from src.dev.plot.axis import AxisConfigurator
from src.dev.plot.config import PlotConfigurator
from src.dev.plot.hover import HoverConfigurator
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParam
from src.service.calc_utils.moving_avg import calc_moving_avg
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
        self.fig, self.ax = plt.subplots(figsize=self.FIG_SIZE)
        PlotConfigurator(self.fig, self.ax).apply()
        HoverConfigurator(self.fig, self.ax, self.ut_period).apply()
        AxisConfigurator(self.ax, self.ut_period).apply()

    def plot_euel(self, station: EeIndexStation, color: str) -> None:
        service = IntermagEuelService(
            StationParam(station=station, period=self.ut_period), Region.BRAZIL
        )
        data = service.get_euel_data_by_range()
        smoothed_array = calc_moving_avg(
            np.array(data.array, dtype=float), window=90, nan_threshold=30
        )


        x = np.arange(len(data.array))
        y = smoothed_array

        self.ax.plot(x, y, label=f"{station.code}_EUEL", color=color)

    @staticmethod
    def _calc_tick_interval(length: int) -> int:
        return max(1, length // 10)

    def set_title(self, title: str) -> None:
        self.ax.set_title(title, fontsize=15, fontweight="semibold", pad=10)

    def show(self) -> None:
        self.ax.legend(loc="lower left", fontsize=10)
        plt.draw()
        plt.show()
        plt.close()

    def save(self, path: str) -> None:
        self.ax.legend(loc="lower left", fontsize=12)
        self.fig.savefig(path, dpi=300)
        self.fig.clf()


if __name__ == "__main__":

    from datetime import datetime, timedelta

    from src.domain.region import Region
    from src.service.eej.best_euel_selector import BestEuelSelectorFactory
    from src.service.eej.calc.eej_detection import EejDetection
    from src.service.eej.calc.euel_diff import calc_euel_peak_diff
    from src.service.eej.load_peculiar_eej import load_peculiar_eej_dates
    from src.service.eej.peculiar_eej_classification import PeculiarEejClassifier
    from src.utils.path import generate_parent_abs_path

    # service = PeculiarEejService()
    # data_list = service.get_by_region(Region.BRAZIL)

    dates = load_peculiar_eej_dates(region=Region.BRAZIL)
    dip_stations = [EeIndexStation.TTB]
    offdip_stations = [EeIndexStation.EUS]
    region = Region.BRAZIL

    for d in dates:
        period = Period(
            start=datetime(d.year, d.month, d.day, 0, 0),
            end=datetime(d.year, d.month, d.day, 23, 59),
        )

        plotter = KatoEuelPlotter(period)

        plotter.plot_euel(EeIndexStation.EUS, "red")
        plotter.plot_euel(EeIndexStation.TTB, "blue")
        # plotter.plot_euel(EeIndexStation.KOU, "green")

        classifier = PeculiarEejClassifier(region=Region.BRAZIL)
        times = [
            datetime.combine(d, datetime.min.time()) + timedelta(minutes=i)
            for i in range(1440)
        ]

        # 使用するEUELのデータを取得
        dip_euel_selector = BestEuelSelectorFactory().create(
            region, dip_stations, d, is_dip=True
        )
        offdip_euel_selector = BestEuelSelectorFactory().create(
            region, offdip_stations, d, is_dip=False
        )

        dip_euel_selector = dip_euel_selector.select_best_euel_data()
        offdip_euel = offdip_euel_selector.select_best_euel_data()
        peak_diff = calc_euel_peak_diff(dip_euel_selector, offdip_euel, d)
        # EEJの種類を分類
        eej_detection = EejDetection(peak_diff, d, region)
        eej_type = eej_detection.classify_eej_category()
        peculiar_eej_type = classifier.classify_peculiar_eej_type(
            times, dip_euel_selector, offdip_euel
        )

        plotter.set_title("Brazil Region EUEL on " + d.strftime("%Y/%m/%d"))
        # plotter.show()

        path = generate_parent_abs_path(
            f"/img/peculiar_eej/brazil_region_by_kato/{peculiar_eej_type.value}/{d.strftime('%Y%m%d')}.png"
        )
        plotter.save(path)
