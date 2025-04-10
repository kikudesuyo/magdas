from datetime import date, datetime, timedelta
from glob import glob

import numpy as np
from src.service.ee_index.constant.magdas_station import EeIndexStation
from src.service.ee_index.constant.raw_data import MAX_H, MIN_H
from src.service.ee_index.constant.time_relation import Min
from src.service.ee_index.helper.raw_data_reader import read_raw_min_data
from src.utils.path import generate_parent_abs_path


class HComponent:
    @staticmethod
    def read_for_day(station_code: str, ut_date: date):
        year, month, day = (
            ut_date.strftime("%Y"),
            ut_date.strftime("%m"),
            ut_date.strftime("%d"),
        )
        filenames = glob(
            generate_parent_abs_path(
                f"/Storage/{station_code}/Min/{year}/{station_code}_MIN_{year}{month}{day}*.mgd"
            )
        )
        try:
            if not filenames:
                raise FileNotFoundError(
                    f"File not found for {station_code} at {ut_date}"
                )
            h_for_day = read_raw_min_data(filenames[0])[:, 0]
            for i in range(Min.ONE_DAY.const):
                if h_for_day[i] <= MIN_H or h_for_day[i] >= MAX_H:
                    h_for_day[i] = np.NaN
            return h_for_day
        except FileNotFoundError as e:
            h_for_day = np.full(Min.ONE_DAY.const, np.NaN)
            return h_for_day
        except ValueError as e:
            h_for_day = np.full(Min.ONE_DAY.const, np.NaN)
            return h_for_day

    @staticmethod
    def get_h_component(station_code, start_dt: datetime, end_dt: datetime):
        """ "任意の時刻から指定した日数分のH値を取得する"""
        start_date, end_date = start_dt.date(), end_dt.date()
        if start_date == end_date:
            start_idx = start_dt.hour * Min.ONE_HOUR.const + start_dt.minute
            end_idx = end_dt.hour * Min.ONE_HOUR.const + end_dt.minute
            day_h_data = HComponent.read_for_day(station_code, start_date)[
                start_idx : end_idx + 1
            ]
            return day_h_data
        h_values = np.array([], dtype=np.float32)
        for i in range((end_date - start_date).days + 1):
            current_date = start_date + timedelta(days=i)
            day_h_data = HComponent.read_for_day(station_code, current_date)
            if current_date == start_date:
                start_idx = start_dt.hour * Min.ONE_HOUR.const + start_dt.minute
                h_values = np.concatenate((h_values, day_h_data[start_idx:]))
            elif current_date == end_date:
                end_idx = end_dt.hour * Min.ONE_HOUR.const + end_dt.minute
                h_values = np.concatenate((h_values, day_h_data[: end_idx + 1]))
            else:
                h_values = np.concatenate((h_values, day_h_data))
        return h_values

    @staticmethod
    def interpolate_h(station: EeIndexStation, start_dt: datetime, end_dt: datetime):
        # TODO h componentはEE-indexだけで使用するわけではないので, stationの型はMagdasStation等にするのが適当。
        h_value = HComponent.get_h_component(station.code, start_dt, end_dt)
        equational_h_component = h_value / np.cos(np.deg2rad(station.gm_lat))
        return equational_h_component

    @staticmethod
    def _handle_file_not_found_error(number_of_elements):
        h_component = np.full(number_of_elements, np.NaN)
        return h_component
