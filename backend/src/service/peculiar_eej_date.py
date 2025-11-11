from src.domain.region import Region
from src.repository.peculiar_eej import PeculiarEejRepository


class PeculiarEejService:
    def __init__(self):
        self.repository = PeculiarEejRepository()

    def get_all(self):
        return self.repository.select_all()

    def get_by_region(self, region: Region):
        return self.repository.select_by_region(region)
