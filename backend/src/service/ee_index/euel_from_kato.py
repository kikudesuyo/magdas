from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period
from src.repository.ee_from_kato import KatoEeRepository


class BrazilEuelDataService:
    def __init__(self, station: EeIndexStation):
        self.repository = KatoEeRepository(station)

    def get_euel_data_by_range(self, period: Period) -> list[float]:
        data = self.repository.select_by_range(period)
        return [item.euel_data for item in data]
