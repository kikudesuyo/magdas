"""特異型EEJの月齢別発生割合をプロット"""

from collections import defaultdict
from datetime import datetime, time
from typing import List

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pydantic import BaseModel
from src.dev.plot.config import PlotConfig
from src.domain.region import Region
from src.domain.station_params import Period
from src.service.eej_category import EejCategoryService
from src.service.lunar_phase import get_lunar_time
from src.service.peculiar_eej import PeculiarEejService


class LunarBinData(BaseModel):
    lunar_time: int  # 月齢(0~23)
    peculiar_eej_count: int  # 特異型EEJ件数
    quiet_count: int  # 静穏日件数

    @property
    def ratio(self) -> float:
        """特異型EEJ発生割合 (%)"""
        if self.quiet_count == 0:
            return 0.0
        return self.peculiar_eej_count / self.quiet_count * 100


class PeculiarEejLunarTimePlotter:
    def __init__(self, region: Region, peculiar_eej_type: str):
        period = Period(
            start=datetime(2009, 1, 1),
            end=datetime(2020, 12, 31),
        )

        peculiar_eej_service = PeculiarEejService()
        self.peculiar_eej_data = peculiar_eej_service.get_by_region_and_type(
            region=region, peculiar_eej_type=peculiar_eej_type
        )

        # 静穏日の月齢の分母を取得するためにEejCategoryServiceを呼び出す
        eej_category_service = EejCategoryService()
        quiet_data = eej_category_service.get_category_by_period_and_type(
            period,
            eej_type="quiet",
        )
        self.quiet_dates = {entry.date for entry in quiet_data}

    def build_lunar_bins(self) -> List[LunarBinData]:
        """
        LunarBinData のリストを作成する。
        静穏日を分母、特異型EEJを分子にする
        """
        # 分母：静穏日の月齢 bin
        quiet_counter: defaultdict[int, int] = defaultdict(int)
        for date in self.quiet_dates:
            lunar_hour = int(get_lunar_time(datetime.combine(date, time.min)))
            quiet_counter[lunar_hour] += 1

        # 分子：特異型EEJの月齢 bin
        peculiar_counter: defaultdict[int, int] = defaultdict(int)
        for eej in self.peculiar_eej_data:
            lunar_hour = int(get_lunar_time(datetime.combine(eej.date, time.min)))
            peculiar_counter[lunar_hour] += 1

        # すべての bin を統合
        all_bins = sorted(set(quiet_counter.keys()) | set(peculiar_counter.keys()))

        # LunarBinData のリストを作成
        return [
            LunarBinData(
                lunar_time=b,
                quiet_count=quiet_counter.get(b, 0),
                peculiar_eej_count=peculiar_counter.get(b, 0),
            )
            for b in all_bins
        ]

    def plot_peculiar_ratio(self, title: str):
        lunar_bins = self.build_lunar_bins()
        x = [d.lunar_time for d in lunar_bins]
        ratio = [d.ratio for d in lunar_bins]

        PlotConfig.rcparams()
        plt.figure(figsize=(10, 6))

        bars = plt.bar(x, ratio, width=1, edgecolor="black")
        for bar, bin_data in zip(bars, lunar_bins):
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{bin_data.peculiar_eej_count}/{bin_data.quiet_count}",
                ha="center",
                va="bottom",
                fontsize=8,
            )

        plt.margins(x=0)
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
        plt.xlabel("Lunar Time")
        plt.ylabel("Peculiar EEJ Ratio (%)")
        plt.grid(True)
        plt.title(title)

    def show(self):
        plt.show()

    def save(self, filename: str):
        plt.savefig(f"img/peculiar_eej/{filename}")


if __name__ == "__main__":

    # 未発達型のプロット"""
    undev_plotter = PeculiarEejLunarTimePlotter(Region.SOUTH_AMERICA, "未発達型")
    undev_plotter.plot_peculiar_ratio(
        title="南アメリカ地域 未発達型EEJ発生割合",
    )
    undev_plotter.show()
    # undev_plotter.save(
    #     filename="2009-2020_南アメリカ_未発達型_月齢.png",
    # )
    # 突発型のプロット"""
    sudden_plotter = PeculiarEejLunarTimePlotter(Region.SOUTH_AMERICA, "突発型")
    sudden_plotter.plot_peculiar_ratio(
        title="南アメリカ地域 突発型EEJ発生割合",
    )
    # sudden_plotter.save(
    #     filename="2009-2020_南アメリカ_突発型_月齢.png",
    # )
    sudden_plotter.show()
