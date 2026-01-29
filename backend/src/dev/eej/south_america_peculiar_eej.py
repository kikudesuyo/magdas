from typing import List

from src.domain.magdas_station import EeIndexStation
from src.domain.region import Region
from src.domain.station_params import Period
from src.model.peculiar_eej import PeculiarEejModel
from src.repository.peculiar_eej import PeculiarEejRepository
from src.service.eej.peculiar_eej_classification import (
    ClassificationPeculiarEej,
    LoadedClassificationPeculiarEej,
)
from src.service.peculiar_eej import PeculiarEejService


class SouthAmericaClassificationPeculiarEej:
    """南アメリカ地域の特異型EEJの分類を行い、CSV操作を行うクラス"""

    def __init__(self, lt_period: Period):
        self.lt_period = lt_period

    def get_peculiar_eej_data(self, type) -> List[PeculiarEejModel]:
        """すでに未発達型と突発型に分類された特異型EEJデータを取得"""
        repository = PeculiarEejRepository()
        return repository.select(
            region=Region.SOUTH_AMERICA,
            type_=type,
            start_date=self.lt_period.start,
            end_date=self.lt_period.end,
        )

    def classify_peculiar_eej_data(self) -> List[PeculiarEejModel]:
        """特異型EEJデータを未発達型と突発型に分類して取得"""
        classification = LoadedClassificationPeculiarEej(
            lt_period=self.lt_period,
            dip_stations=[EeIndexStation.ANC, EeIndexStation.HUA],
            offdip_stations=[EeIndexStation.EUS],
            region=Region.SOUTH_AMERICA,
        )
        peculiar_eej_data_list = classification.aggregate_peculiar_eej_data()
        print(peculiar_eej_data_list)
        return peculiar_eej_data_list

    def save_data(self, is_loaded: bool):
        if is_loaded:
            classification = LoadedClassificationPeculiarEej(
                lt_period=self.lt_period,
                dip_stations=[EeIndexStation.ANC, EeIndexStation.HUA],
                offdip_stations=[EeIndexStation.EUS],
                region=Region.SOUTH_AMERICA,
            )
            PeculiarEejService().save_peculiar_eej(
                classification.aggregate_peculiar_eej_data()
            )

        classification = ClassificationPeculiarEej(
            lt_period=self.lt_period,
            dip_stations=[EeIndexStation.ANC, EeIndexStation.HUA],
            offdip_stations=[EeIndexStation.EUS],
            region=Region.SOUTH_AMERICA,
        )
        peculiar_eej_data_list = classification.aggregate_peculiar_eej_data()
        PeculiarEejService().save_peculiar_eej(peculiar_eej_data_list)


if __name__ == "__main__":
    from datetime import datetime

    lt_period = Period(datetime(2021, 1, 1, 0, 0), datetime(2021, 1, 3, 23, 59))
    classification = SouthAmericaClassificationPeculiarEej(lt_period)
    classification.save_data(is_loaded=True)
    # classification.classify_peculiar_eej_data(type="peculiar")
