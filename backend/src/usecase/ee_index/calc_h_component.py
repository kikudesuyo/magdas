from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from src.domain.station_params import StationParams
from src.repository.gm_data import GMPeriodRepository


@dataclass
class HData:
    ut_params: StationParams
    h_values: NDArray[np.float64]


class HComponent:
    def __init__(self, ut_params: StationParams):
        self.gm_repo = GMPeriodRepository(ut_params)
        self.ut_params = ut_params

    def get_equatorial_h(self) -> HData:
        """指定された観測点のh成分を、磁気赤道（gm_lat=0）の値に換算"""
        # TODO h componentはEE-indexだけで使用するわけではないので, stationの型はMagdasStation等にするのが適当。
        h_values = self.gm_repo.get("h")
        equatorial_h_component = h_values / np.cos(
            np.deg2rad(self.ut_params.station.gm_lat)
        )
        return HData(ut_params=self.ut_params, h_values=equatorial_h_component)
