from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from src.domain.station_params import Period


def main(period: Period):
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
    plt.savefig("data/south_america_euel_peak_diff_histgram.png")
    plt.close()


if __name__ == "__main__":
    period = Period(
        start=datetime(2016, 1, 1, 0, 0),
        end=datetime(2020, 12, 31, 23, 59),
    )
    main(period)
