from datetime import date, datetime, timedelta
from glob import glob

import numpy as np
from src.service.ee_index.constant.magdas_station import EeIndexStation
from src.service.ee_index.constant.raw_data import MAX_H, MIN_H
from src.service.ee_index.constant.time_relation import Min
from src.service.ee_index.helper.raw_data_reader import read_raw_min_data
from src.utils.path import generate_parent_abs_path


def get_h_for_a_day(station_code: str, ut_date: date):
    year = ut_date.strftime("%Y")
    month = ut_date.strftime("%m")
    day = ut_date.strftime("%d")
    filenames = glob(
        generate_parent_abs_path(
            f"/Storage/{station_code}/Min/{year}/{station_code}_MIN_{year}{month}{day}*.mgd"
        )
    )
    if len(filenames) == 0:
        h_for_day = np.full(Min.ONE_DAY.const, np.NaN)
        return h_for_day
    if len(filenames) > 1:
        raise FileNotFoundError(
            f"Multiple files found for {station_code} at {ut_date}: {filenames}"
        )
    try:
        h_for_day = read_raw_min_data(filenames[0])[:, 0]
        for i in range(Min.ONE_DAY.const):
            if h_for_day[i] <= MIN_H or h_for_day[i] >= MAX_H:
                h_for_day[i] = np.NaN
        return h_for_day
    except ValueError as e:  # ファイルのデータ形式によるエラーが発生する場合がある
        h_for_day = np.full(Min.ONE_DAY.const, np.NaN)
        return h_for_day


class HComponent:
    @staticmethod
    def get_h_component(station_code, start_ut: datetime, end_ut: datetime):
        start_date, end_date = start_ut.date(), end_ut.date()
        if start_date == end_date:
            start_idx = start_ut.hour * Min.ONE_HOUR.const + start_ut.minute
            end_idx = end_ut.hour * Min.ONE_HOUR.const + end_ut.minute
            day_h_data = get_h_for_a_day(station_code, start_date)[
                start_idx : end_idx + 1
            ]
            return day_h_data
        h_values = np.array([], dtype=np.float32)
        for i in range((end_date - start_date).days + 1):
            current_date = start_date + timedelta(days=i)
            day_h_data = get_h_for_a_day(station_code, current_date)
            if current_date == start_date:
                start_idx = start_ut.hour * Min.ONE_HOUR.const + start_ut.minute
                h_values = np.concatenate((h_values, day_h_data[start_idx:]))
            elif current_date == end_date:
                end_idx = end_ut.hour * Min.ONE_HOUR.const + end_ut.minute
                h_values = np.concatenate((h_values, day_h_data[: end_idx + 1]))
            else:
                h_values = np.concatenate((h_values, day_h_data))
        return h_values

    @staticmethod
    def to_equatorial_h(station: EeIndexStation, start_ut: datetime, end_ut: datetime):
        """指定された観測点のh成分を、磁気赤道（gm_lat=0）での値に換算"""
        # TODO h componentはEE-indexだけで使用するわけではないので, stationの型はMagdasStation等にするのが適当。
        h_value = HComponent.get_h_component(station.code, start_ut, end_ut)
        equational_h_component = h_value / np.cos(np.deg2rad(station.gm_lat))
        return equational_h_component
