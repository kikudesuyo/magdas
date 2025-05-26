import numpy as np
from src.domain.station_params import StationParams
from src.repository.gm_data import GMPeriodRepository


class HComponent:
    def __init__(self, params: StationParams):
        self.params = params
        self.station = params.station
        self.start_ut = params.period.start
        self.end_ut = params.period.end

    def get_h_component(self):
        """指定された観測点のh成分を取得"""
        gm_repo = GMPeriodRepository(self.params)
        h_values = gm_repo.get("h")
        return h_values

    def to_equatorial_h(self):
        """指定された観測点のh成分を、磁気赤道（gm_lat=0）での値に換算"""
        # TODO h componentはEE-indexだけで使用するわけではないので, stationの型はMagdasStation等にするのが適当。
        h_value = self.get_h_component()
        equatorial_h_component = h_value / np.cos(np.deg2rad(self.station.gm_lat))
        return equatorial_h_component
