import csv
from datetime import datetime, timedelta

import numpy as np
from numpy.typing import NDArray
from src.domain.station_params import EeIndexStation, Period
from src.service.ee_index.calc_eej_detection import (
    BestEuelSelectorForEej,
    DaytimeInterval,
)


def get_timestamp(start: datetime, end: datetime) -> NDArray[np.datetime64]:
    return np.array(
        [
            start + timedelta(minutes=i)
            for i in range(int((end - start).total_seconds() / 60) + 1)
        ]
    )


def write_dip_station_peak_euel_to_csv(
    writer, ut_period: Period, dip_station: EeIndexStation
):
    """EEJ検知のための昼間の最大のEUELを計算"""
    current_date = ut_period.start.date()
    while current_date <= ut_period.end.date():
        euel_selector = BestEuelSelectorForEej([dip_station], current_date, is_dip=True)
        euel_data = euel_selector.select_euel_data()

        day_start = datetime.combine(current_date, datetime.min.time())
        day_end = day_start + timedelta(days=1) - timedelta(minutes=1)
        timestamp = get_timestamp(day_start, day_end)

        is_noon = np.array([DaytimeInterval.contains(dt.time()) for dt in timestamp])
        filtered = euel_data.array[is_noon]
        max_euel = np.max(filtered) if filtered.size > 0 else np.nan

        writer.writerow([current_date.isoformat(), dip_station.code, max_euel])
        current_date += timedelta(days=1)


def write_offdip_station_peak_euel_to_csv(
    writer, ut_period: Period, offdip_station: EeIndexStation
):
    """EEJ検知のための昼間の最大のEUELを計算"""
    current_date = ut_period.start.date()
    while current_date <= ut_period.end.date():
        euel_selector = BestEuelSelectorForEej(
            [offdip_station], current_date, is_dip=False
        )
        euel_data = euel_selector.select_euel_data()

        day_start = datetime.combine(current_date, datetime.min.time())
        day_end = day_start + timedelta(days=1) - timedelta(minutes=1)
        timestamp = get_timestamp(day_start, day_end)

        is_noon = np.array([DaytimeInterval.contains(dt.time()) for dt in timestamp])
        filtered = euel_data.array[is_noon]
        max_euel = np.max(filtered) if filtered.size > 0 else np.nan

        writer.writerow([current_date.isoformat(), offdip_station.code, max_euel])
        current_date += timedelta(days=1)


ut_param = Period(
    start=datetime(2000, 1, 1),
    end=datetime(2022, 12, 31),
)


bcl = EeIndexStation.BCL
cdo = EeIndexStation.CDO
ceb = EeIndexStation.CEB
dav = EeIndexStation.DAV
gsi = EeIndexStation.GSI
lgz = EeIndexStation.LGZ
lkw = EeIndexStation.LKW
lwa = EeIndexStation.LWA
mnd = EeIndexStation.MND
mut = EeIndexStation.MUT
scn = EeIndexStation.SCN
tgg = EeIndexStation.TGG
yap = EeIndexStation.YAP


dip_stations = [bcl, cdo, ceb, dav, lkw, yap]
dip_path = "data/southeast_asia_dip_station_peak_euel.csv"
with open(dip_path, "a", newline="", buffering=1) as f:
    writer = csv.writer(f)
    writer.writerow(["date", "station_code", "peak_euel"])
    for station in dip_stations:
        write_dip_station_peak_euel_to_csv(writer, ut_param, station)


offdip_stations = [gsi, lgz, mnd, mut, scn, tgg]


offdip_path = "data/southeast_asia_offdip_station_peak_euel.csv"
with open(offdip_path, "a", newline="", buffering=1) as f:
    writer = csv.writer(f)
    # writer.writerow(["date", "station_code", "peak_euel"])
    for station in offdip_stations:
        write_offdip_station_peak_euel_to_csv(writer, ut_param, station)
