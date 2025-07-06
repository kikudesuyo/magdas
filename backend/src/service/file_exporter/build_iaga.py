from datetime import datetime, timedelta

import pandas as pd
from src.constants.time_relation import TimeUnit
from src.domain.magdas_station import EeIndexStation


def build_iaga_meta_data(station: EeIndexStation, iaga_code, elevation):
    return {
        "Format": "IAGA-2002",
        "Source of Data": "Kyushu University (KU)",
        "Station Name": f"{station.code}",
        "IAGA CODE": f"{iaga_code} (KU code)",
        "Geodetic Latitude": station.gm_lat,
        "Geodetic Longitude": station.gm_lon,
        "Elevation": elevation,
        "Reported": "EE-index",
        "Recorded data": "EE-index: EDst1h, EDst6h, ER_HUA, EUEL_HUA",
        "Digital Sampling": "1 second",
        "Data Interval Type": "Averaged 1-minute (00:30 - 01:29)",
        "Data Type": "Provisional EE-index:230202",
    }


def build_iaga_data(
    start_ut: datetime,
    end_ut: datetime,
    edst_1h_values,
    edst_6h_values,
    er_values,
    euel_values,
):
    days = (end_ut - start_ut).days + 1

    return {
        "DATE": [
            (start_ut + timedelta(days=j)).strftime("%Y-%m-%d")
            for j in range(days)
            for _ in range(TimeUnit.ONE_DAY.min)
        ],
        "TIME": [
            f"{(i % TimeUnit.ONE_DAY.min) // TimeUnit.ONE_HOUR.min:02d}:{(i % TimeUnit.ONE_DAY.min) % TimeUnit.ONE_MINUTE.sec:02d}:00.000"
            for i in range(TimeUnit.ONE_DAY.min * days)
        ],
        "DOY": [
            (start_ut + timedelta(days=j)).timetuple().tm_yday
            for j in range(days)
            for _ in range(TimeUnit.ONE_DAY.min)
        ],
        "EDst1h": edst_1h_values,
        "EDst6h": edst_6h_values,
        "ER": er_values,
        "EUEL": euel_values,
    }


def save_as_iaga(iaga_meta_data, iaga_data, file_name):
    df = pd.DataFrame(iaga_data)
    with open(file_name, "w") as f:
        # メタデータ
        for key, value in iaga_meta_data.items():
            f.write(f"{key:<25} {value:<40}\n")
        # ッダー
        f.write(
            f"{'DATE':<11}{'TIME':<13}{'DOY':<7}{'EDst1h':<10}{'EDst6h':<10}{'ER':<10}{'EUEL':<10}\n"
        )
        # データ
        for _, row in df.iterrows():
            f.write(
                f"{row['DATE']:<11}{row['TIME']:<13}{str(row['DOY']).zfill(3):<7}{row['EDst1h']:<10.2f}{row['EDst6h']:<10.2f}{row['ER']:<10.2f}{row['EUEL']:<10.2f}\n"
            )
