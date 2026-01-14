import numpy as np
from src.domain.region import Region
from src.domain.station_params import StationParam
from src.model.euel_data import EuelData
from src.repository.ee_from_kato import KatoEeRepository


class IntermagEuelService:
    def __init__(self, param: StationParam, region: Region):
        self.kato_repo = KatoEeRepository(param.station)
        self.ut_params = param
        self.region = region

    def get_euel_data_by_range(self) -> EuelData:
        data = self.kato_repo.select_by_range(self.ut_params.period)
        array = np.array([item.euel_data for item in data], dtype=float)
        return EuelData(region=self.region, station=self.ut_params.station, array=array)
