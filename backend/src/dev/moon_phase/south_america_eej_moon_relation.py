import csv
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
from pydantic import BaseModel
from src.domain.station_params import Period
from src.service.calc_moon_phase import calc_moon_phase
from utils.path import generate_parent_abs_path


class MoonPhaseData(BaseModel):
    moon_age: float
    nan_cnt: int = 0
    disturbance_cnt: int = 0
    normal_eej_cnt: int = 0
    peculiar_eej_cnt: int = 0
    total_cnt: int = 0


def aggregate_peculiar_ratio(
    period: Period,
    csv_path: Optional[str] = None,
) -> Tuple[List[float], List[float]]:
    """
    CSVを読み込んで期間内のデータを集計し、月齢binごとのpeculiar EEJ割合(%)を返す。

    Returns:
        Tuple[x: List[moon_age_bin], y: List[peculiar_ratio_percent]]
    """
    BIN_SIZE = 1  # 月齢の区切り幅（例: 0.5日ごとに集計）

    if csv_path is None:
        csv_path = generate_parent_abs_path(
            "/src/dev/moon_phase/south_america_eej_category.csv"
        )

    moon_phase_d: Dict[float, MoonPhaseData] = {}

    with open(csv_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date_str = row["date"]
            category = row["category"]

            dt = datetime.strptime(date_str, "%Y-%m-%d")

            if dt < period.start:
                continue
            if dt > period.end:
                continue
            moon_age_bin = calc_moon_phase(dt)
            moon_age_bin = round(moon_age_bin / BIN_SIZE) * BIN_SIZE

            if moon_age_bin not in moon_phase_d:
                moon_phase_d[moon_age_bin] = MoonPhaseData(moon_age=moon_age_bin)

            data = moon_phase_d[moon_age_bin]
            if category == "missing":
                data.nan_cnt += 1
            elif category == "disturbance":
                data.disturbance_cnt += 1
            elif category == "normal":
                data.normal_eej_cnt += 1
            elif category == "peculiar":
                data.peculiar_eej_cnt += 1
            data.total_cnt += 1

    sorted_bins = sorted(moon_phase_d.items())
    bins = [bin_key for bin_key, _ in sorted_bins]

    peculiar_ratios = []
    for _, data in sorted_bins:
        valid_total = data.normal_eej_cnt + data.peculiar_eej_cnt
        if valid_total == 0:
            peculiar_ratios.append(0)
        else:
            ratio = data.peculiar_eej_cnt / valid_total * 100
            peculiar_ratios.append(ratio)

    return bins, peculiar_ratios


def plot_peculiar_ratio(
    x: List[float], peculiar_ratio: List[float], title_suffix: str = ""
):
    plt.figure(figsize=(12, 6))
    plt.bar(
        x,
        peculiar_ratio,
        width=0.4,  # 固定幅
        color="deepskyblue",
        label="Peculiar EEJ Ratio",
    )

    plt.xlabel("Moon Age (days)")
    plt.ylabel("Peculiar EEJ Ratio (%)")
    plt.title(f"Peculiar EEJ Ratio by Moon Phase {title_suffix}")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()


period = Period(start=datetime(2014, 1, 1), end=datetime(2020, 12, 31))
x, y = aggregate_peculiar_ratio(period)


plot_peculiar_ratio(
    x, y, title_suffix=f"from {period.start.date()} to {period.end.date()}"
)
