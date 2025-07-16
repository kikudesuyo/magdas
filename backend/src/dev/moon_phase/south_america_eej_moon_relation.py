from datetime import datetime
from typing import List, Tuple

import matplotlib.pyplot as plt
import pandas as pd
from src.domain.station_params import Period
from src.service.calc_moon_phase import calc_moon_phase
from utils.path import generate_parent_abs_path


def aggregate_peculiar_ratio_by_moon_age(
    period: Period,
    csv_path: str,
) -> Tuple[List[float], List[float]]:
    BIN_SIZE = 1
    df = pd.read_csv(csv_path, parse_dates=["date"])
    df = df[(df["date"] >= period.start) & (df["date"] <= period.end)]

    df["moon_age"] = df["date"].apply(calc_moon_phase)
    df["moon_age_bin"] = (df["moon_age"] / BIN_SIZE).round() * BIN_SIZE

    grouped = df.groupby(["moon_age_bin", "category"]).size().unstack(fill_value=0)

    bins = sorted(grouped.index.tolist())
    peculiar_ratios = []

    for bin_val in bins:
        normal = grouped.at[bin_val, "normal"] if "normal" in grouped.columns else 0
        peculiar = (
            grouped.at[bin_val, "peculiar"] if "peculiar" in grouped.columns else 0
        )
        valid_total = normal + peculiar
        ratio = (peculiar / valid_total * 100) if valid_total > 0 else 0
        peculiar_ratios.append(ratio)

    return bins, peculiar_ratios


def plot_peculiar_ratio(
    x: List[float], peculiar_ratio: List[float], title_suffix: str = ""
):
    plt.figure(figsize=(12, 6))
    plt.bar(
        x,
        peculiar_ratio,
        width=0.4,
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
path = generate_parent_abs_path("/src/dev/south_america_eej_category.csv")
x, y = aggregate_peculiar_ratio_by_moon_age(period, path)


plot_peculiar_ratio(
    x, y, title_suffix=f"from {period.start.date()} to {period.end.date()}"
)
