from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from src.domain.station_params import Period
from src.service.calc_eej_detection import EejDetection
from src.utils.path import generate_parent_abs_path


def load_and_prepare_df(path: str, station_code: str, period: Period) -> dict:
    # 'nan'などの文字列を欠損値(NaN)として認識させる
    df = pd.read_csv(
        path,
        parse_dates=["date"],
        na_values=["nan", "NaN", "NULL", ""],
    )
    # 数値化しておく（文字列だったら強制NaN）
    df["peak_euel"] = pd.to_numeric(df["peak_euel"], errors="coerce")
    df = df[
        (df["date"] >= period.start)
        & (df["date"] <= period.end)
        & (df["station_code"] == station_code)
    ][["date", "peak_euel"]]

    # 日付をキーに辞書化（datetime.date -> float）
    return {row["date"].date(): row["peak_euel"] for _, row in df.iterrows()}


def main():
    dip_path = generate_parent_abs_path(
        "/Storage/peak_euel/southeast_asia_dip_station_peak_euel.csv"
    )
    offdip_path = generate_parent_abs_path(
        "/Storage/peak_euel/southeast_asia_offdip_station_peak_euel.csv"
    )

    period = Period(start=datetime(2016, 1, 1), end=datetime(2016, 12, 31))

    dip_dict = load_and_prepare_df(dip_path, "DAV", period)
    offdip_dict = load_and_prepare_df(offdip_path, "MND", period)

    results = []

    dt = period.start
    while dt <= period.end:
        key = dt.date()
        dip_val = dip_dict.get(key)
        offdip_val = offdip_dict.get(key)

        if dip_val is None or offdip_val is None:
            dt += timedelta(days=1)
            continue

        if pd.isna(dip_val) or pd.isna(offdip_val):
            peak_diff = np.nan
        else:
            peak_diff = dip_val - offdip_val

        eej_detection = EejDetection(peak_diff=peak_diff, local_date=dt)
        category = eej_detection.classify_eej_category()

        if category.label == "peculiar":
            print(f"{key} is a peculiar EEJ")

        results.append(
            {
                "date": key,
                "peak_diff": peak_diff,
                "eej_category": category.label,
            }
        )

        dt += timedelta(days=1)

    # 必要に応じてCSVに保存
    result_df = pd.DataFrame(results)
    result_df.to_csv("eej_detection_results.csv", index=False)


if __name__ == "__main__":
    main()
