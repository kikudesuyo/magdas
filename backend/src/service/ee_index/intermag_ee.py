from src.domain.station_params import StationParam
from src.repository.ee_from_kato import KatoEeRepository


class IntermagEuelService:
    def __init__(self, ut_params: StationParam):
        self.kato_repo = KatoEeRepository(ut_params.station)
        self.ut_params = ut_params

    def get_euel_data_by_range(self) -> list[float]:
        data = self.kato_repo.select_by_range(self.ut_params.period)
        return [item.euel_data for item in data]
