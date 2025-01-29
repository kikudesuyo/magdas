from datetime import date, datetime, timedelta
from glob import glob

import numpy as np
from src.ee_index.constant.magdas_station import EeIndexStation
from src.ee_index.constant.raw_data import MAX_H, MIN_H
from src.ee_index.constant.time_relation import Min
from src.ee_index.helper.raw_data_reader import read_raw_min_data
from src.ee_index.path import generate_parent_abs_path


class HComponent:
    @staticmethod
    def read_for_day(station, ut_date: date):
        year, month, day = (
            ut_date.strftime("%Y"),
            ut_date.strftime("%m"),
            ut_date.strftime("%d"),
        )
        filenames = glob(
            generate_parent_abs_path(
                f"/Storage/{station}/Min/{year}/{station}_MIN_{year}{month}{day}*.mgd"
            )
        )
        try:
            if not filenames:
                raise FileNotFoundError(f"File not found for {station} at {ut_date}")
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
    def get_h_for_days(station, datetime: datetime, days: int) -> np.ndarray:
        """ "任意の時刻から指定した日数分のH値を取得する"""
        date, hour, minute = (
            datetime.date(),
            datetime.hour,
            datetime.minute,
        )
        initial_index = hour * Min.ONE_HOUR.const + minute
        total_index = days * Min.ONE_DAY.const
        h_component_value = np.array([], dtype=np.float32)
        for day in range(days + 1):
            try:
                if day == 0:
                    h_component_value = HComponent.read_for_day(station, date)[
                        initial_index:
                    ]
                elif day == days:
                    h_component_value = np.concatenate(
                        (
                            h_component_value,
                            HComponent.read_for_day(
                                station, date + timedelta(days=day)
                            )[:initial_index],
                        )
                    )
                    if total_index != len(h_component_value):
                        raise ValueError(
                            f"total_index: {total_index}, len(h_component_value): {len(h_component_value)}"
                        )
                    return h_component_value
                else:
                    h_component_value = np.concatenate(
                        (
                            h_component_value,
                            HComponent.read_for_day(
                                station, date + timedelta(days=day)
                            ),
                        )
                    )
            except FileNotFoundError as e:
                print(e)
                if day == 0:
                    offset = Min.ONE_DAY.const - initial_index
                else:
                    offset = Min.ONE_DAY.const
                h_component_value = np.concatenate(
                    (
                        h_component_value,
                        HComponent._handle_file_not_found_error(offset),
                    )
                )
        return h_component_value

    @staticmethod
    def interpolate_h_component(station, datetime, days):
        h_component = HComponent.get_h_for_days(station, datetime, days)
        gm_latitude = EeIndexStation[station].gm_lat
        equational_h_component = h_component / np.cos(np.deg2rad(gm_latitude))
        return equational_h_component

    @staticmethod
    def _handle_file_not_found_error(number_of_elements):
        h_component = np.full(number_of_elements, np.NaN)
        return h_component
