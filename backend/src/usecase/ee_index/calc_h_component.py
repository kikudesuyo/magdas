from datetime import timedelta

import numpy as np
from src.constants.time_relation import TimeUnit
from src.domain.station_params import StationParams
from src.repository.gm_data import GMDataLoader


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
            gm_loader = GMDataLoader(self.station.code, start_date)
            day_h_data = gm_loader.h[start_idx : end_idx + 1]
            return day_h_data
        h_values = np.array([], dtype=np.float32)
        for i in range((end_date - start_date).days + 1):
            current_date = start_date + timedelta(days=i)
            gm_loader = GMDataLoader(self.station.code, current_date)
            day_h_data = gm_loader.h
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
        equatorial_h_component = h_value / np.cos(np.deg2rad(self.station.gm_lat))
        return equatorial_h_component
