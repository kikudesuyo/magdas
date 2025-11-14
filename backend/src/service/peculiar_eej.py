from src.domain.region import Region
from src.repository.peculiar_eej import PeculiarEejRepository


class PeculiarEejService:
    def __init__(self):
        self.repository = PeculiarEejRepository()

    def get_by_region(self, region: Region):
        return self.repository.select(region=region)

    def get_by_region_and_type(self, region: Region, type: str):
        return self.repository.select(region=region, type_=type)
