"""月ごとの特異型EEJ発生割合をプロット"""

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
from src.service.peculiar_eej import PeculiarEejService


class MonthBinData(BaseModel):
    month: int  # 月(1~12)
    peculiar_eej_count: int  # 特異型EEJ件数
    quiet_count: int  # 静穏日件数

    @property
    def ratio(self) -> float:
        """特異型EEJ発生割合 (%)"""
        if self.quiet_count == 0:
            return 0.0
        return self.peculiar_eej_count / self.quiet_count * 100


class PeculiarEejMonthPlotter:
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

    def build_month_bins(self) -> List[MonthBinData]:
        """
        MonthBinData のリストを作成する。
        静穏日を分母、特異型EEJを分子にする
        """
        # 分母：静穏日の月 bin
        quiet_counter: defaultdict[int, int] = defaultdict(int)
        for date in self.quiet_dates:
            month = date.month
            quiet_counter[month] += 1

        # 分子：特異型EEJの月 bin
        peculiar_counter: defaultdict[int, int] = defaultdict(int)
        for eej in self.peculiar_eej_data:
            dt = datetime.combine(eej.date, time.min)
            month = dt.month
            peculiar_counter[month] += 1

        month_bins: List[MonthBinData] = []
        for month in range(1, 13):
            month_bins.append(
                MonthBinData(
                    month=month,
                    peculiar_eej_count=peculiar_counter.get(month, 0),
                    quiet_count=quiet_counter.get(month, 0),
                )
            )
        return month_bins

    def plot_peculiar_ratio(self, title: str):
        month_bins = self.build_month_bins()
        x = [bin.month for bin in month_bins]
        ratio = [bin.ratio for bin in month_bins]
        PlotConfig.rcparams()
        plt.figure(figsize=(10, 6))

        bars = plt.bar(x, ratio, width=0.6, edgecolor="black")

        for bar, bin_data in zip(bars, month_bins):
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
        plt.xlabel("Month")
        plt.ylabel("Peculiar EEJ Ratio (%)")
        plt.grid(True)
        plt.title(title)

    def show(self):
        plt.show()

    def save(self, filename: str):
        plt.savefig(f"img/peculiar_eej/{filename}")
        plt.close()


if __name__ == "__main__":
    # 突発型のプロット
    sudden_plotter = PeculiarEejMonthPlotter(Region.SOUTH_AMERICA, "突発型")
    sudden_plotter.plot_peculiar_ratio(title="南アメリカ地域 突発型EEJ発生割合")
    # sudden_plotter.save(filename="2009-2020_南アメリカ_突発型_月.png")
    sudden_plotter.show()

    # 未発達型のプロット
    undev_plotter = PeculiarEejMonthPlotter(Region.SOUTH_AMERICA, "未発達型")
    undev_plotter.plot_peculiar_ratio(title="南アメリカ地域 未発達型EEJ発生割合")
    # undev_plotter.save(filename="2009-2020_南アメリカ_未発達型_月.png")
    undev_plotter.show()
