from datetime import datetime
from typing import List, Tuple

import matplotlib.pyplot as plt
import pandas as pd
from src.domain.station_params import Period
from utils.path import generate_parent_abs_path


def aggregate_peculiar_ratio_by_month(
    period: Period,
    csv_path: str,
) -> Tuple[List[str], List[float]]:
    df = pd.read_csv(csv_path, parse_dates=["date"])
    df = df[(df["date"] >= period.start) & (df["date"] <= period.end)]

    # 年は無視して月だけで集計（1〜12）
    df["month"] = df["date"].dt.month

    # 月ごと・カテゴリごとの件数をカウント
    grouped = df.groupby(["month", "category"]).size().unstack(fill_value=0)

    months = list(range(1, 13))
    month_labels = [f"{m}" for m in months]
    peculiar_ratios = []

    for m in months:
        if m not in grouped.index:
            peculiar_ratios.append(0)
            continue
        normal = grouped.at[m, "normal"] if "normal" in grouped.columns else 0
        peculiar = grouped.at[m, "peculiar"] if "peculiar" in grouped.columns else 0
        total = normal + peculiar
        ratio = (peculiar / total * 100) if total > 0 else 0
        peculiar_ratios.append(ratio)

    return month_labels, peculiar_ratios


def plot_peculiar_ratio_by_month(
    months: List[str],
    ratios: List[float],
    title_suffix: str = "",
):
    plt.figure(figsize=(10, 5))
    plt.bar(months, ratios, width=0.6, color="deepskyblue", label="Peculiar EEJ Ratio")

    plt.xlabel("Month")
    plt.ylabel("Peculiar EEJ Ratio (%)")
    plt.title(f"Peculiar EEJ Ratio by Calendar Month {title_suffix}")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(
        generate_parent_abs_path(
            f"/data/south_america_eej_peculiar_ratio_by_month{title_suffix}.png"
        )
    )
    # plt.show()


# ==== 実行 ====

period = Period(start=datetime(2014, 1, 1), end=datetime(2020, 12, 31))
path = generate_parent_abs_path("/src/dev/south_america_eej_category.csv")

months, ratios = aggregate_peculiar_ratio_by_month(period, path)

plot_peculiar_ratio_by_month(
    months, ratios, title_suffix=f"(from {period.start.year} to {period.end.year})"
)
