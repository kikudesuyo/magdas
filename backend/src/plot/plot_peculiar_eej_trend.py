from datetime import date, datetime

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
from src.service.moon_phase import get_lunar_age, get_lunar_time
from src.utils.path import generate_parent_abs_path


def plot_undev_histogram(undev_dates: list[date]):
    df = pd.DataFrame({"date": undev_dates})
    df["month"] = pd.to_datetime(df["date"]).dt.month

    # 月ごとの出現回数をカウント（1~12月すべて）
    month_counts = df["month"].value_counts().sort_index()
    month_counts = month_counts.reindex(range(1, 13), fill_value=0)

    # ヒストグラムではなく棒グラフで描画
    plt.bar(month_counts.index, month_counts.values, edgecolor="black", width=0.6)
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    plt.xlabel("Month")
    plt.ylabel("Count of UNDEVELOPED type")
    plt.title("Monthly Histogram of UNDEVELOPED Peculiar EEJ")
    plt.xticks(range(1, 13))  # 1~12月を明示
    plt.tight_layout()
    p = generate_parent_abs_path("/data/undev_histogram_south_america.png")
    plt.savefig(p)
    # plt.show()


def plot_sudden_histogram(moon_phase_list: list[float | int]):
    # 横軸は月齢
    df = pd.DataFrame({"moon_phase": moon_phase_list})
    df["moon_phase_bin"] = (df["moon_phase"] // 1) * 1  # 1日刻みでビン分け
    moon_phase_counts = df["moon_phase_bin"].value_counts().sort_index()
    moon_phase_counts = moon_phase_counts.reindex(range(0, 24), fill_value=0)

    bins = [x - 0.5 for x in range(25)]

    plt.hist(df["moon_phase"], bins=bins, edgecolor="black", align="mid")

    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    plt.title("Histogram of SUDDEN Peculiar EEJ by Moon Phase")
    plt.xlabel("Lunar Time (Hour)")
    plt.ylabel("Frequency")
    # plt.show()
    p = generate_parent_abs_path("/data/sudden_eej_moon_phase_histogram.png")
    plt.savefig(p)


def load_peculiar_eej_dates(peculiar_eej_type, region) -> list[date]:
    path = "peculiar_eej_classification.csv"
    df = pd.read_csv(path, parse_dates=["Date"])
    filtered_df = df[(df["Type"] == peculiar_eej_type) & (df["Station"] == region)]

    dates = filtered_df["Date"].dt.date.tolist()
    return [d if isinstance(d, date) else pd.to_datetime(d).date() for d in dates]


if __name__ == "__main__":
    # 未発達型EEJのヒストグラム
    # peculiar_eej_dates = load_peculiar_eej_dates("未発達型", "south_america")
    # plot_undev_histogram(peculiar_eej_dates)
    # 突然変異型EEJのヒストグラム
    peculiar_eej_dates = load_peculiar_eej_dates("突発型", "south_america")
    peculiar_eej_datetimes = [
        datetime.combine(d, datetime.min.time()) for d in peculiar_eej_dates
    ]
    lunar_ages = [get_lunar_age(d) for d in peculiar_eej_datetimes]
    # moon_phase_list = [get_lunar_age(d) for d in peculiar_eej_datetimes]
    lunar_time_list = [get_lunar_time(d) for d in peculiar_eej_datetimes]

    print(lunar_time_list)

    plot_sudden_histogram(lunar_time_list)
