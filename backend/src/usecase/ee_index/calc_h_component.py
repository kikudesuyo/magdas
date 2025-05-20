from datetime import date, timedelta
from glob import glob

import numpy as np
from src.constants.ee_index import MAX_RAW_H, MIN_RAW_H
from src.constants.time_relation import TimeUnit
from src.domain.station_params import StationParams
from src.usecase.raw_data_reader import read_raw_min_data
from src.utils.path import generate_parent_abs_path


def get_h_for_a_day(station_code: str, ut_date: date):
    year = ut_date.strftime("%Y")
    month = ut_date.strftime("%m")
    day = ut_date.strftime("%d")
    filenames = glob(
        generate_parent_abs_path(
            f"/Storage/ee_index/{station_code}/Min/{year}/{station_code}_MIN_{year}{month}{day}*.mgd"
        )
    )
    if len(filenames) == 0:
        h_for_day = np.full(TimeUnit.ONE_DAY.min, np.NaN)
        return h_for_day
    if len(filenames) > 1:
        raise FileNotFoundError(
            f"Multiple files found for {station_code} at {ut_date}: {filenames}"
        )
    try:
        h_for_day = read_raw_min_data(filenames[0])[:, 0]
        for i in range(TimeUnit.ONE_DAY.min):
            if h_for_day[i] <= MIN_RAW_H or h_for_day[i] >= MAX_RAW_H:
                h_for_day[i] = np.NaN
        return h_for_day
    except ValueError as e:  # ファイルのデータ形式によるエラーが発生する場合がある
        h_for_day = np.full(TimeUnit.ONE_DAY.min, np.NaN)
        return h_for_day


class HComponent:
    def __init__(self, params: StationParams):
        self.station = params.station
        self.start_ut = params.period.start
        self.end_ut = params.period.end

    def get_h_component(self):
        start_date, end_date = self.start_ut.date(), self.end_ut.date()
        if start_date == end_date:
            start_idx = (
                self.start_ut.hour * TimeUnit.ONE_HOUR.min + self.start_ut.minute
            )
            end_idx = self.end_ut.hour * TimeUnit.ONE_HOUR.min + self.end_ut.minute
            day_h_data = get_h_for_a_day(self.station.code, start_date)[
                start_idx : end_idx + 1
            ]
            return day_h_data
        h_values = np.array([], dtype=np.float32)
        for i in range((end_date - start_date).days + 1):
            current_date = start_date + timedelta(days=i)
            day_h_data = get_h_for_a_day(self.station.code, current_date)
            if current_date == start_date:
                start_idx = (
                    self.start_ut.hour * TimeUnit.ONE_HOUR.min + self.start_ut.minute
                )
                h_values = np.concatenate((h_values, day_h_data[start_idx:]))
            elif current_date == end_date:
                end_idx = self.end_ut.hour * TimeUnit.ONE_HOUR.min + self.end_ut.minute
                h_values = np.concatenate((h_values, day_h_data[: end_idx + 1]))
            else:
                h_values = np.concatenate((h_values, day_h_data))
        return h_values

    def to_equatorial_h(self):
        """指定された観測点のh成分を、磁気赤道（gm_lat=0）での値に換算"""
        # TODO h componentはEE-indexだけで使用するわけではないので, stationの型はMagdasStation等にするのが適当。
        h_value = self.get_h_component()
        equational_h_component = h_value / np.cos(np.deg2rad(self.station.gm_lat))
        return equational_h_component
