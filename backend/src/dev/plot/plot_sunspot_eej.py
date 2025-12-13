"""太陽活動度と特異型EEJの関係をプロット"""

from datetime import datetime, time, timedelta
from typing import List

from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter, DayLocator
from src.dev.plot.config import PlotConfigurator
from src.domain.magdas_station import EeIndexStation
from src.domain.region import Region
from src.domain.station_params import Period
from src.service.eej.best_euel_selector import BestEuelSelectorFactory
from src.service.sunspot import Sunspot


class SunspotPlotter:
    def __init__(self, lt_period: Period):
        self.lt_period = lt_period
        self.fig, (self.ax_sunspot, self.ax_eej) = plt.subplots(
            nrows=2, ncols=1, figsize=(15, 8), sharex=False  # sharex=Falseに変更
        )
        PlotConfigurator(self.fig, self.ax_sunspot).apply()
        PlotConfigurator(self.fig, self.ax_eej).apply()

    def _validate_period(self):
        if self.lt_period.start.time() != time(
            0, 0
        ) or self.lt_period.end.time() != time(23, 59):
            raise ValueError("start_lt must be 00:00 and end_lt must be 23:59.")

    def plot_sunspot(self, color):
        start, end = self.lt_period.start, self.lt_period.end
        sunspot_data = Sunspot().get_sunspot_by_range(start, end)
        self.ax_sunspot.set_ylabel("Sunspot (F10.7)", rotation=0, labelpad=50)
        self.ax_sunspot.plot(
            sunspot_data["Date"],
            sunspot_data["F10.7"],
            label="Sunspot",
            color=color,
            marker="o",
            markersize=3,
            linewidth=1.5,
        )
        self.ax_sunspot.legend(loc="upper left")
        self.ax_sunspot.grid(True, alpha=0.3)

        # X軸の設定（sunspot用）
        self.ax_sunspot.set_xlim(start, end)

        # 日付フォーマットの設定
        if (end - start).days > 60:  # 2ヶ月以上の場合
            self.ax_sunspot.xaxis.set_major_formatter(DateFormatter("%m/%d"))
        else:
            self.ax_sunspot.xaxis.set_major_formatter(DateFormatter("%m/%d"))

    def plot_euel_to_detect_eej(
        self, region: Region, stations: List[EeIndexStation], color, is_dip: bool
    ):
        """EEJを検知するためのプロット - 1分データをそのまま表示
        注意:
        EEJの検知は日毎で行うため、start_ltとend_ltは日付の粒度で指定してください
        """
        self._validate_period()

        # 日付範囲を生成
        date_range = [
            self.lt_period.start.date() + timedelta(days=i)
            for i in range((self.lt_period.end - self.lt_period.start).days + 1)
        ]

        # EEJデータとそれに対応するdatetimeを生成
        euel_data = []
        datetime_data = []

        for date in date_range:
            daily_euel = (
                BestEuelSelectorFactory()
                .create(region, stations, date, is_dip)
                .select_best_euel_data()
                .array
            )
            euel_data.extend(daily_euel)

            # 各分に対応するdatetimeを生成（1日1440分）
            for minute in range(len(daily_euel)):
                dt = datetime.combine(date, time(0, 0)) + timedelta(minutes=minute)
                datetime_data.append(dt)

        """_summary_
        """  # 全データをプロット（圧縮なし）
        label = (
            f"{'dip' if is_dip else 'offdip'}({', '.join([s.code for s in stations])})"
        )

        # 大量データの場合は線のみ（マーカーなし）でプロット
        self.ax_eej.plot(
            datetime_data, euel_data, label=label, color=color, linewidth=0.8, alpha=0.8
        )

        self.ax_eej.set_ylabel("EEJ Value")
        self.ax_eej.legend(loc="upper left")
        self.ax_eej.grid(True, alpha=0.3)

        # X軸の設定（EEJ用）
        self.ax_eej.set_xlim(self.lt_period.start, self.lt_period.end)

        """_summary_
        """  # EEJ用の日付フォーマット設定
        if (self.lt_period.end - self.lt_period.start).days > 60:
            self.ax_eej.xaxis.set_major_locator(DayLocator(interval=7))
            self.ax_eej.xaxis.set_major_formatter(DateFormatter("%m/%d"))
        else:
            self.ax_eej.xaxis.set_major_locator(DayLocator(interval=3))
            self.ax_eej.xaxis.set_major_formatter(DateFormatter("%m/%d"))

    def plot_euel_subsampled_for_display(
        self,
        region: Region,
        stations: List[EeIndexStation],
        color,
        is_dip: bool,
        subsample_minutes: int = 10,
    ):
        """表示用にサブサンプリングしたEEJデータをプロット（元データは保持）
        subsample_minutes: サンプリング間隔（分）
        """
        self._validate_period()

        date_range = [
            self.lt_period.start.date() + timedelta(days=i)
            for i in range((self.lt_period.end - self.lt_period.start).days + 1)
        ]

        euel_data = []
        datetime_data = []

        for date in date_range:
            daily_euel = (
                BestEuelSelectorFactory()
                .create(region, stations, date, is_dip)
                .select_best_euel_data()
                .array
            )

            # サブサンプリング（指定した間隔でデータを取得）
            for minute in range(0, len(daily_euel), subsample_minutes):
                if minute < len(daily_euel):
                    euel_data.append(daily_euel[minute])
                    dt = datetime.combine(date, time(0, 0)) + timedelta(minutes=minute)
                    datetime_data.append(dt)

        label = (
            f"{'dip' if is_dip else 'offdip'}({', '.join([s.code for s in stations])})"
        )

        self.ax_eej.plot(
            datetime_data,
            euel_data,
            label=label,
            color=color,
            linewidth=1,
            alpha=0.9,
            marker=".",
            markersize=1,
        )

        self.ax_eej.set_ylabel("EEJ Value")
        self.ax_eej.legend(loc="upper left")
        self.ax_eej.grid(True, alpha=0.3)
        self.ax_eej.set_xlim(self.lt_period.start, self.lt_period.end)

        # X軸ラベルを表示
        self.ax_eej.tick_params(axis="x", which="major", labelsize=10)
        plt.setp(self.ax_eej.xaxis.get_majorticklabels(), rotation=45)

    def set_title(self, title):
        self.fig.suptitle(title, fontsize=15, fontweight="semibold", y=0.95)

    def show(self):
        # 各軸の日付フォーマットを設定（重複設定を削除）
        plt.tight_layout()
        plt.show()

    def save(self, path):
        self.fig.autofmt_xdate()
        plt.tight_layout()
        plt.savefig(path, dpi=300, bbox_inches="tight")
        plt.close(self.fig)


# 使用例
if __name__ == "__main__":
    from datetime import datetime

    dip_stations = [EeIndexStation.ANC, EeIndexStation.HUA]
    offdip_stations = [EeIndexStation.EUS]
    region = Region.SOUTH_AMERICA

    start = datetime(2017, 1, 1, 0, 0)
    end = datetime(2017, 12, 31, 23, 59)
    ut_period = Period(start, end)
    d = SunspotPlotter(ut_period)

    # sunspotデータ（日次）をプロット
    d.plot_sunspot("blue")

    # # # 方法1: 全EEJデータ（1分間隔）をプロット - 大容量注意
    # d.plot_euel_to_detect_eej(region, dip_stations, "red", is_dip=True)

    # # 方法2: 表示用にサブサンプリング（推奨）
    # d.plot_euel_subsampled_for_display(
    #     region, dip_stations, "red", is_dip=True, subsample_minutes=10
    # )

    d.set_title(f"SSW Temperature Plot {2017}")
    d.show()
    # d.save(f"img/ssw_plot_{2017}.png")
