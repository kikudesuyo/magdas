"""前後10%にラインを引いてヒストグラムを描画"""

from dataclasses import dataclass
from datetime import datetime
from typing import List

import matplotlib.pyplot as plt
import pandas as pd
from src.domain.magdas_station import EeIndexStation
from src.domain.region import Region
from src.domain.station_params import Period, StationParam
from src.service.ee_index.intermag_ee import IntermagEuelService
from src.service.eej.calc.euel_diff import calc_euel_peak_diff


@dataclass
class PeakEuel:
    dip_station: EeIndexStation
    offdip_station: EeIndexStation
    date: datetime
    diff: float


class BrazilHistgramPlotter:
    def __init__(self, period: Period):
        self.period = period

    def plot_brazil_histgram(self):
        peak_euel_diff_list = self.get_peak_euel_diff()

        plt.figure(figsize=(10, 6))
        import matplotlib.ticker as mticker

        plt.hist(
            peak_euel_diff_list,
            bins=range(
                int(min(peak_euel_diff_list)) - 5,
                int(max(peak_euel_diff_list)) + 5,
                5,
            ),
            edgecolor="black",
        )
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
        plt.title(
            f"Brazil Peak EUEL Difference Distribution({period.start.strftime('%Y-%m-%d')} to {period.end.strftime('%Y-%m-%d')})"
        )
        plt.xlabel("Peak EUEL Difference")
        plt.ylabel("Frequency")
        plt.grid(True)

        # Calculate and plot 80% confidence interval
        lower_bound = pd.Series(peak_euel_diff_list).quantile(0.10)
        upper_bound = pd.Series(peak_euel_diff_list).quantile(0.90)
        plt.axvline(
            lower_bound,
            color="r",
            linestyle="--",
            linewidth=2,
            label=f"10th percentile: {lower_bound:.2f}",
        )
        plt.axvline(
            upper_bound,
            color="r",
            linestyle="--",
            linewidth=2,
            label=f"90th percentile: {upper_bound:.2f}",
        )
        plt.legend()
        plt.savefig("data/brazil_euel_peak_diff_histgram_2009_2020.png")
        # plt.show()
        plt.close()

    def get_euel_peak_euel(self) -> List[PeakEuel]:
        start = self.period.start
        end = self.period.end

        peak_euel_list = []
        for date in pd.date_range(start.date(), end.date()):
            period = Period(
                start=datetime(date.year, date.month, date.day, 0, 0),
                end=datetime(date.year, date.month, date.day, 23, 59),
            )
            ttb_param = StationParam(station=EeIndexStation.TTB, period=period)
            eus_param = StationParam(station=EeIndexStation.EUS, period=period)
            ttb_service = IntermagEuelService(param=ttb_param, region=Region.BRAZIL)
            dip_euel = ttb_service.get_euel_data_by_range()
            eus_service = IntermagEuelService(param=eus_param, region=Region.BRAZIL)
            offdip_euel = eus_service.get_euel_data_by_range()

            peak_diff = calc_euel_peak_diff(dip_euel, offdip_euel, date.date())
            peak_euel = PeakEuel(
                dip_station=EeIndexStation.TTB,
                offdip_station=EeIndexStation.EUS,
                date=date.to_pydatetime(),
                diff=peak_diff,
            )
            peak_euel_list.append(peak_euel)
        return peak_euel_list

    def extract_quiet_days(self) -> List[datetime]:
        disturbance_df = pd.read_csv("Storage/disturbance.csv", skipinitialspace=True)
        disturbance_df["date"] = pd.to_datetime(disturbance_df["date"])
        quiet_df = disturbance_df[disturbance_df["category"] == "quiet"]
        quiet_df = quiet_df[
            (quiet_df["date"] >= self.period.start)
            & (quiet_df["date"] <= self.period.end)
        ]
        return [d.date() for d in quiet_df["date"]]

    def extract_valid_peak_euel(self, peak_euel_list: List[PeakEuel]) -> List[PeakEuel]:
        return [p for p in peak_euel_list if not pd.isna(p.diff)]

    def get_peak_euel_diff(self) -> List[float]:
        peak_euel_list = self.get_euel_peak_euel()
        extracted_nan_peak_euel = self.extract_valid_peak_euel(peak_euel_list)
        quiet_dates = self.extract_quiet_days()

        peak_euel_diff_list: list[float] = []
        for peak_euel in extracted_nan_peak_euel:
            if peak_euel.date.date() in quiet_dates:
                peak_euel_diff_list.append(peak_euel.diff)
        return peak_euel_diff_list


def south_america_histgram(period: Period):
    dip_df = pd.read_csv(
        "Storage/peak_euel/south_america_dip_station_peak_euel.csv",
        skipinitialspace=True,
    )
    offdip_df = pd.read_csv(
        "Storage/peak_euel/south_america_offdip_station_peak_euel.csv",
        skipinitialspace=True,
    )

    dip_df["date"] = pd.to_datetime(dip_df["date"])
    offdip_df["date"] = pd.to_datetime(offdip_df["date"])

    disturbance_df = pd.read_csv("Storage/disturbance.csv", skipinitialspace=True)
    disturbance_df["date"] = pd.to_datetime(disturbance_df["date"])
    quiet_df = disturbance_df[disturbance_df["category"] == "quiet"]

    dip_df = dip_df[(dip_df["date"] >= period.start) & (dip_df["date"] <= period.end)]
    offdip_df = offdip_df[
        (offdip_df["date"] >= period.start) & (offdip_df["date"] <= period.end)
    ]

    # Group by date and calculate the mean for the dip stations
    dip_df_mean = dip_df.groupby("date")["peak_euel"].mean().reset_index()

    merged_df = pd.merge(
        dip_df_mean, offdip_df, on="date", suffixes=("_dip_mean", "_offdip")
    )
    merged_df = pd.merge(merged_df, quiet_df, on="date")

    peak_euel_dip = merged_df["peak_euel_dip_mean"]
    peak_euel_offdip = merged_df["peak_euel_offdip"]
    peak_euel_diff = peak_euel_dip - peak_euel_offdip

    merged_df["peak_euel_diff"] = peak_euel_diff

    negative_diff_dates = merged_df[merged_df["peak_euel_diff"] < 0]["date"]

    print("Dates with negative peak EUEL difference:")
    for date in negative_diff_dates:
        print(date.strftime("%Y-%m-%d"))

    print("\nDates with peak EUEL difference < -25:")
    large_negative_diff_df = merged_df[merged_df["peak_euel_diff"] < -25]
    for index, row in large_negative_diff_df.iterrows():
        print(f"{row['date'].strftime('%Y-%m-%d')}: {row['peak_euel_diff']}")

    plt.figure(figsize=(10, 6))
    import matplotlib.ticker as mticker

    plt.hist(
        merged_df["peak_euel_diff"].dropna(),
        bins=range(
            int(merged_df["peak_euel_diff"].min()) - 5,
            int(merged_df["peak_euel_diff"].max()) + 5,
            5,
        ),
        edgecolor="black",
    )
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    plt.title(
        f"Peak EUEL Difference Distribution({period.start.strftime('%Y-%m-%d')} to {period.end.strftime('%Y-%m-%d')})"
    )
    plt.xlabel("Peak EUEL Difference")
    plt.ylabel("Frequency")
    plt.grid(True)

    # Calculate and plot 80% confidence interval
    lower_bound = merged_df["peak_euel_diff"].quantile(0.10)
    upper_bound = merged_df["peak_euel_diff"].quantile(0.90)
    plt.axvline(
        lower_bound,
        color="r",
        linestyle="--",
        linewidth=2,
        label=f"10th percentile: {lower_bound:.2f}",
    )
    plt.axvline(
        upper_bound,
        color="r",
        linestyle="--",
        linewidth=2,
        label=f"90th percentile: {upper_bound:.2f}",
    )
    plt.legend()

    plt.savefig("data/south_america_euel_peak_diff_histgram_2009_2020.png")
    plt.close()


if __name__ == "__main__":
    period = Period(
        start=datetime(2009, 1, 1, 0, 0),
        end=datetime(2020, 12, 31, 23, 59),
    )

    brazil_plotter = BrazilHistgramPlotter(period)
    # brazil_plotter.plot_brazil_histgram()

    south_america_histgram(period)
