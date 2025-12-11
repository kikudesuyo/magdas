from typing import List

from src.domain.magdas_station import EeIndexStation
from src.domain.region import Region
from src.domain.station_params import Period
from src.model.peculiar_eej import PeculiarEejModel
from src.repository.peculiar_eej import PeculiarEejRepository
from src.service.eej.peculiar_eej_classification import ClassificationPeculiarEej


class BrazilClassificationPeculiarEej:
    """ブラジル地域の特異型EEJの分類を行い、CSV操作を行うクラス"""

    def __init__(self, lt_period: Period):
        self.lt_period = lt_period

    def get_peculiar_eej_data(self, type) -> List[PeculiarEejModel]:
        repository = PeculiarEejRepository()
        return repository.select(
            region=Region.BRAZIL,
            type_=type,
            start_date=self.lt_period.start,
            end_date=self.lt_period.end,
        )

    def add_data(self):
        classification = ClassificationPeculiarEej(
            lt_period=self.lt_period,
            dip_stations=[EeIndexStation.TTB],
            offdip_stations=[EeIndexStation.EUS, EeIndexStation.KOU],
            region=Region.BRAZIL,
        )
        classification.add_data()
