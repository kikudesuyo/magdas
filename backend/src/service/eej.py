from datetime import date
from typing import List

from src.domain.region import Region
from src.repository.peculiar_eej import PeculiarEejRepository


class PeculiarEejService:
    def __init__(self):
        self.repo = PeculiarEejRepository()

    def get_dates_by_region(self, region: Region) -> List[date]:
        return self.repo.select_by_region(region)
