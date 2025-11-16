from typing import List

from src.domain.region import Region
from src.model.peculiar_eej import PeculiarEejModel
from src.repository.peculiar_eej import PeculiarEejRepository


class PeculiarEejService:
    def __init__(self):
        self.repo = PeculiarEejRepository()

    def get_by_region(self, region: Region):
        return self.repo.select(region=region)

    def get_by_region_and_type(self, region: Region, type: str):
        return self.repo.select(region=region, type_=type)

    def add_peculiar_eej(self, peculiar_eej: List[PeculiarEejModel]):
        self.repo.insert(peculiar_eej)
