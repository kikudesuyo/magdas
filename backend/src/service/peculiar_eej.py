from typing import List

from src.domain.region import Region
from src.domain.station_params import Period
from src.model.peculiar_eej import PeculiarEejModel
from src.repository.peculiar_eej import PeculiarEejRepository


class PeculiarEejService:
    def __init__(self):
        self.repo = PeculiarEejRepository()

    def get_by_region(self, region: Region):
        return self.repo.select(region=region)

    def get_by_region_and_type(self, region: Region, peculiar_eej_type: str):
        return self.repo.select(region=region, type_=peculiar_eej_type)

    def get_by_period_and_region_and_type(
        self, period: Period, region: Region, peculiar_eej_type: str
    ):
        return self.repo.select(
            region=region,
            type_=peculiar_eej_type,
            start_date=period.start,
            end_date=period.end,
        )

    def add_peculiar_eej(self, peculiar_eej: List[PeculiarEejModel]):
        self.repo.insert(peculiar_eej)
